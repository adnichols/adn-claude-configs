#!/usr/bin/env python3
"""
Documentation Fetch Script for Claude Code
Fetches and processes documentation from various sources into AI-friendly Markdown format.
"""

import argparse
import os
import sys
import time
import subprocess
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json
import re
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocsFetcher:
    """Main class for fetching and processing documentation."""
    
    def __init__(self, base_dir: str = "/workspace/docs"):
        self.base_dir = Path(base_dir)
        self.user_agent = 'Mozilla/5.0 (compatible; Claude-Code-DocsFetch/1.0; +https://claude.ai/code)'
        
        # Rate limiting configuration
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0.0
        
        # Site patterns for common documentation sites
        self.site_patterns = self._load_site_patterns()
    
    def _load_site_patterns(self) -> Dict:
        """Load site-specific parsing patterns."""
        patterns_file = Path(__file__).parent / "site-patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r') as f:
                return json.load(f)
        
        # Default patterns for common documentation sites
        return {
            "react.dev": {
                "selectors": {
                    "main_content": "main[role='main']",
                    "navigation": "nav[role='navigation']",
                    "title": "h1"
                },
                "base_urls": ["https://react.dev/"],
                "sections": ["learn", "reference", "community"]
            },
            "docs.python.org": {
                "selectors": {
                    "main_content": ".body-content",
                    "navigation": ".toctree-wrapper",
                    "title": "h1"
                },
                "base_urls": ["https://docs.python.org/3/"],
                "sections": ["tutorial", "library", "reference"]
            },
            "developer.mozilla.org": {
                "selectors": {
                    "main_content": ".main-page-content",
                    "navigation": ".document-toc",
                    "title": "h1"
                },
                "base_urls": ["https://developer.mozilla.org/en-US/docs/"],
                "sections": ["Web", "JavaScript", "CSS", "HTML"]
            }
        }
    
    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe filesystem storage."""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename.strip('._')
    
    def _determine_library_type(self, library_name: str) -> str:
        """Determine if library is a framework, language, or library."""
        frameworks = {'react', 'vue', 'angular', 'nextjs', 'nuxt', 'svelte', 'express', 'fastapi', 'django', 'flask'}
        languages = {'python', 'javascript', 'typescript', 'rust', 'go', 'java', 'cpp', 'c', 'php'}
        
        library_lower = library_name.lower()
        
        if library_lower in frameworks:
            return 'frameworks'
        elif library_lower in languages:
            return 'languages'
        else:
            return 'libraries'
    
    def _create_directory_structure(self, library_name: str) -> Path:
        """Create appropriate directory structure for the library."""
        library_type = self._determine_library_type(library_name)
        lib_dir = self.base_dir / library_type / library_name.lower()
        lib_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (lib_dir / 'examples').mkdir(exist_ok=True)
        
        return lib_dir
    
    def _discover_documentation_urls(self, library_name: str) -> List[str]:
        """Discover official documentation URLs for a given library."""
        # Common URL patterns for documentation
        common_patterns = [
            f"https://{library_name.lower()}.dev/",
            f"https://docs.{library_name.lower()}.org/",
            f"https://{library_name.lower()}.org/docs/",
            f"https://{library_name.lower()}.readthedocs.io/",
            f"https://developer.mozilla.org/en-US/docs/Web/{library_name}",
            f"https://github.com/{library_name}/{library_name}/tree/main/docs"
        ]
        
        # Special cases for well-known libraries
        special_cases = {
            'react': ['https://react.dev/'],
            'vue': ['https://vuejs.org/guide/'],
            'angular': ['https://angular.dev/'],
            'python': ['https://docs.python.org/3/'],
            'javascript': ['https://developer.mozilla.org/en-US/docs/Web/JavaScript'],
            'typescript': ['https://www.typescriptlang.org/docs/'],
            'lodash': ['https://lodash.com/docs/'],
            'express': ['https://expressjs.com/'],
            'nextjs': ['https://nextjs.org/docs']
        }
        
        if library_name.lower() in special_cases:
            return special_cases[library_name.lower()]
        
        # Test common patterns to find working URLs
        working_urls = []
        for url in common_patterns:
            try:
                self._enforce_rate_limit()
                # Use curl to test URL accessibility
                result = subprocess.run([
                    'curl', '-s', '-I', '--connect-timeout', '10', 
                    '-H', f'User-Agent: {self.user_agent}', url
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and 'HTTP/' in result.stdout and '200' in result.stdout:
                    working_urls.append(url)
                    logger.info(f"Found working URL: {url}")
            except (subprocess.SubprocessError, subprocess.TimeoutExpired):
                continue
        
        return working_urls[:3]  # Limit to first 3 working URLs
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a single URL with error handling."""
        try:
            self._enforce_rate_limit()
            logger.info(f"Fetching content from: {url}")
            
            # Use curl to fetch content
            result = subprocess.run([
                'curl', '-s', '--connect-timeout', '30', '--max-time', '60',
                '-H', f'User-Agent: {self.user_agent}', url
            ], capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"curl failed for {url}: {result.stderr}")
                return None
        
        except (subprocess.SubprocessError, subprocess.TimeoutExpired) as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def parse_arguments(self, args_string: str) -> Tuple[str, Dict]:
        """Parse command line arguments from string."""
        # Split the arguments string into components
        args = args_string.strip().split()
        
        if not args:
            raise ValueError("No library name provided")
        
        library_name = args[0]
        options = {}
        
        # Parse optional flags
        i = 1
        while i < len(args):
            if args[i].startswith('--'):
                flag = args[i][2:]  # Remove '--'
                if i + 1 < len(args) and not args[i + 1].startswith('--'):
                    options[flag] = args[i + 1]
                    i += 2
                else:
                    options[flag] = True
                    i += 1
            else:
                i += 1
        
        return library_name, options
    
    def create_metadata(self, library_name: str, urls: List[str], version: str = None) -> Dict:
        """Create metadata for the documentation."""
        return {
            'library': library_name,
            'version': version or 'latest',
            'source_urls': urls,
            'last_fetched': time.strftime('%Y-%m-%d'),
            'completeness': 0,  # Will be updated after processing
            'ai_optimized': True
        }
    
    def fetch_documentation(self, library_name: str, **options) -> bool:
        """Main method to fetch documentation for a library."""
        try:
            logger.info(f"Starting documentation fetch for: {library_name}")
            
            # Create directory structure
            lib_dir = self._create_directory_structure(library_name)
            
            # Discover documentation URLs
            urls = self._discover_documentation_urls(library_name)
            if not urls:
                logger.warning(f"No documentation URLs found for {library_name}")
                return False
            
            # Create metadata
            metadata = self.create_metadata(library_name, urls, options.get('version'))
            
            # For Phase 1, we'll create a basic index file with discovered URLs
            # This will be expanded in later phases
            self._create_index_file(lib_dir, library_name, metadata, urls)
            
            logger.info(f"Documentation structure created for {library_name} in {lib_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {library_name}: {str(e)}")
            return False
    
    def _create_index_file(self, lib_dir: Path, library_name: str, metadata: Dict, urls: List[str]):
        """Create initial index file with metadata and discovered URLs."""
        index_content = f"""---
library: "{metadata['library']}"
version: "{metadata['version']}"
source_urls:
{chr(10).join(f'  - "{url}"' for url in metadata['source_urls'])}
last_fetched: "{metadata['last_fetched']}"
completeness: {metadata['completeness']}
ai_optimized: {metadata['ai_optimized']}
---

# {library_name.title()} Documentation

## Overview

This directory contains AI-optimized documentation for {library_name}, fetched from official sources and converted to Markdown format for enhanced Claude Code integration.

## Source URLs

The following official documentation sources were identified:

{chr(10).join(f'- [{url}]({url})' for url in urls)}

## Structure

- `index.md` - This overview file
- `api-reference.md` - Complete API documentation (to be generated)
- `best-practices.md` - Current patterns and conventions (to be generated)
- `examples/` - Practical implementation examples (to be generated)

## Status

- ✅ Directory structure created
- ✅ Source URLs identified
- ⏳ Content fetching (Phase 2)
- ⏳ Content processing (Phase 2)
- ⏳ AI optimization (Phase 2)

*Last updated: {metadata['last_fetched']}*
"""
        
        index_file = lib_dir / 'index.md'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        logger.info(f"Created index file: {index_file}")

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python docs-fetch.py <library_name> [options]")
        print("Example: python docs-fetch.py react --version 18.3.0")
        sys.exit(1)
    
    # Parse arguments
    args_string = ' '.join(sys.argv[1:])
    fetcher = DocsFetcher()
    
    try:
        library_name, options = fetcher.parse_arguments(args_string)
        success = fetcher.fetch_documentation(library_name, **options)
        
        if success:
            print(f"✅ Documentation structure created for {library_name}")
            sys.exit(0)
        else:
            print(f"❌ Failed to fetch documentation for {library_name}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()