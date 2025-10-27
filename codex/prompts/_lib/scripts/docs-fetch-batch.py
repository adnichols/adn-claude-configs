#!/usr/bin/env python3
"""
Batch Documentation Fetch Script for Claude Code
Processes markdown lists to extract and fetch documentation for multiple libraries.
"""

import argparse
import os
import sys
import re
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile

# Import the existing docs fetcher
try:
    from docs_fetch import DocsFetcher
except ImportError:
    # If import fails, try to run the existing script directly
    DocsFetcher = None

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarkdownParser:
    """Parses markdown content to extract library information."""

    def __init__(self):
        # Patterns to match markdown bullet points with links
        self.link_patterns = [
            r'\*\s*\[([^\]]+)\]\(([^)]+)\)',  # * [Name](URL)
            r'-\s*\[([^\]]+)\]\(([^)]+)\)',   # - [Name](URL)
            r'\d+\.\s*\[([^\]]+)\]\(([^)]+)\)',  # 1. [Name](URL)
        ]

        # Common version patterns
        self.version_patterns = [
            r'(.+?)\s+v?(\d+(?:\.\d+)*)',  # Name v1.2.3 or Name 1.2.3
            r'(.+?)\s+(\d+(?:\.\d+)*)',     # Name 1.2.3
        ]

        # Non-library patterns to skip
        self.skip_patterns = [
            r'perfect\s+lighthouse\s+score',
            r'bundle\s+analyzer',
            r'github\s+actions',
            r'conventional\s+commits',
            r'observability',
            r'absolute\s+imports',
            r'health\s+checks',
            r'renovate\s+bot',
            r'patch-package',
            r'component\s+relationship\s+tools',
            r'semantic\s+release',
            r'advanced\s+testing',
            r'smoke\s+and\s+acceptance\s+testing',
        ]

        # Library name mappings for common display names
        self.name_mappings = {
            # JavaScript/TypeScript frameworks
            'next.js': 'nextjs',
            'nextjs': 'nextjs',
            'react': 'react',
            'reactjs': 'react',
            'vue.js': 'vue',
            'vuejs': 'vue',
            'vue': 'vue',
            'angular': 'angular',
            'angularjs': 'angular',
            'svelte': 'svelte',

            # CSS frameworks
            'tailwind css': 'tailwindcss',
            'tailwindcss': 'tailwindcss',
            'bootstrap': 'bootstrap',
            'material-ui': 'material-ui',
            'mui': 'material-ui',
            'ant design': 'antd',
            'antd': 'antd',
            'chakra ui': 'chakra-ui',
            'chakra-ui': 'chakra-ui',
            'radix ui': 'radix-ui',
            'radix-ui': 'radix-ui',
            'cva': 'cva',
            'class variance authority': 'cva',

            # Build tools
            'webpack': 'webpack',
            'vite': 'vite',
            'rollup': 'rollup',
            'parcel': 'parcel',
            'esbuild': 'esbuild',

            # Languages
            'typescript': 'typescript',
            'javascript': 'javascript',
            'python': 'python',
            'rust': 'rust',
            'go': 'go',
            'java': 'java',
            'kotlin': 'kotlin',
            'swift': 'swift',
            'dart': 'dart',
            'php': 'php',

            # Testing
            'jest': 'jest',
            'vitest': 'vitest',
            'cypress': 'cypress',
            'playwright': 'playwright',
            'puppeteer': 'puppeteer',
            'selenium': 'selenium',
            'react testing library': 'react-testing-library',
            'testing library': 'testing-library',

            # Code quality
            'eslint': 'eslint',
            'prettier': 'prettier',
            'husky': 'husky',
            'lint-staged': 'lint-staged',

            # Package managers
            'npm': 'npm',
            'yarn': 'yarn',
            'pnpm': 'pnpm',
            'corepack': 'corepack',

            # Documentation
            'storybook': 'storybook',
            'docusaurus': 'docusaurus',
            'gitbook': 'gitbook',

            # Databases
            'mongodb': 'mongodb',
            'mongoose': 'mongoose',
            'postgresql': 'postgresql',
            'postgres': 'postgresql',
            'mysql': 'mysql',
            'redis': 'redis',
            'sqlite': 'sqlite',

            # Node.js frameworks
            'express': 'express',
            'koa': 'koa',
            'fastify': 'fastify',
            'nest': 'nestjs',
            'nestjs': 'nestjs',

            # Python frameworks
            'django': 'django',
            'flask': 'flask',
            'fastapi': 'fastapi',
            'pyramid': 'pyramid',

            # Utilities
            'lodash': 'lodash',
            'moment': 'moment',
            'dayjs': 'dayjs',
            'date-fns': 'date-fns',
            'axios': 'axios',
            'fetch': 'fetch',

            # Environment/Config
            't3 env': 't3-env',
            'dotenv': 'dotenv',

            # Monitoring/Observability
            'opentelemetry': 'opentelemetry',
            'sentry': 'sentry',
            'datadog': 'datadog',

            # Third-party libraries
            'ts-reset': 'ts-reset',
            'bundle analyzer': 'bundle-analyzer',
        }

    def extract_libraries_from_markdown(self, markdown_content: str) -> List[Dict]:
        """Extract library information from markdown content."""
        libraries = []
        lines = markdown_content.split('\n')

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue

            # Try each link pattern
            for pattern in self.link_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for name, url in matches:
                    library_info = self._process_library_match(name, url, line_num, line)
                    if library_info:
                        libraries.append(library_info)

        # Remove duplicates based on mapped name
        seen = set()
        unique_libraries = []
        for lib in libraries:
            if lib['mapped_name'] not in seen:
                seen.add(lib['mapped_name'])
                unique_libraries.append(lib)

        return unique_libraries

    def _process_library_match(self, display_name: str, url: str, line_num: int, full_line: str) -> Optional[Dict]:
        """Process a matched library name and URL."""
        # Clean up the display name
        display_name = display_name.strip()
        url = url.strip()

        # Skip if it matches non-library patterns
        for skip_pattern in self.skip_patterns:
            if re.search(skip_pattern, display_name, re.IGNORECASE):
                logger.debug(f"Skipping non-library item: {display_name}")
                return None

        # Extract version if present
        version = None
        clean_name = display_name

        for pattern in self.version_patterns:
            match = re.match(pattern, display_name, re.IGNORECASE)
            if match:
                clean_name, version = match.groups()
                clean_name = clean_name.strip()
                break

        # Map to standard library name
        mapped_name = self._map_library_name(clean_name)
        if not mapped_name:
            logger.warning(f"Could not map library name: {clean_name}")
            # Use a sanitized version of the clean name as fallback
            mapped_name = re.sub(r'[^a-z0-9\-_]', '-', clean_name.lower()).strip('-')

        return {
            'display_name': display_name,
            'clean_name': clean_name,
            'mapped_name': mapped_name,
            'url': url,
            'version': version,
            'line_number': line_num,
            'full_line': full_line
        }

    def _map_library_name(self, name: str) -> Optional[str]:
        """Map display name to standard library identifier."""
        name_lower = name.lower().strip()

        # Direct mapping
        if name_lower in self.name_mappings:
            return self.name_mappings[name_lower]

        # Try removing common suffixes/prefixes
        variations = [
            name_lower,
            name_lower.replace('.js', ''),
            name_lower.replace('js', ''),
            name_lower.replace('-', ''),
            name_lower.replace('_', ''),
            name_lower.replace(' ', ''),
            name_lower.replace(' ', '-'),
            name_lower.replace(' ', '_'),
        ]

        for variation in variations:
            if variation in self.name_mappings:
                return self.name_mappings[variation]

        # If no mapping found, return sanitized version
        return re.sub(r'[^a-z0-9\-_]', '-', name_lower).strip('-')

class BatchDocsFetcher:
    """Main class for batch documentation fetching."""

    def __init__(self):
        self.parser = MarkdownParser()
        self.docs_fetcher = None
        if DocsFetcher:
            self.docs_fetcher = DocsFetcher()

    def parse_arguments(self, args_string: str) -> Tuple[str, Dict]:
        """Parse command line arguments from string."""
        args = args_string.strip().split()

        if not args:
            raise ValueError("No markdown content provided")

        # Check for --file option
        if '--file' in args:
            file_index = args.index('--file')
            if file_index + 1 < len(args):
                file_path = args[file_index + 1]
                markdown_content = self._read_file(file_path, args)
                args = args[:file_index] + args[file_index + 2:]  # Remove --file and path
            else:
                raise ValueError("--file option requires a file path")
        else:
            # First argument is the markdown content
            markdown_content = args[0]
            args = args[1:]

        # Parse remaining options
        options = {}
        i = 0
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

        return markdown_content, options

    def _read_file(self, file_path: str, args: List[str]) -> str:
        """Read markdown content from file, optionally extracting a section."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for --section option
            if '--section' in args:
                section_index = args.index('--section')
                if section_index + 1 < len(args):
                    section_name = args[section_index + 1]
                    content = self._extract_section(content, section_name)

            return content
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {str(e)}")

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract a specific section from markdown content."""
        lines = content.split('\n')
        section_lines = []
        in_section = False
        section_level = None

        for line in lines:
            if line.strip().startswith('#'):
                # Check if this is our target section
                if section_name.lower() in line.lower():
                    in_section = True
                    section_level = len(line) - len(line.lstrip('#'))
                    section_lines.append(line)
                elif in_section:
                    # Check if we've reached another section at the same or higher level
                    current_level = len(line) - len(line.lstrip('#'))
                    if current_level <= section_level:
                        break
                    else:
                        section_lines.append(line)
                else:
                    continue
            elif in_section:
                section_lines.append(line)

        if not section_lines:
            logger.warning(f"Section '{section_name}' not found in content")
            return content  # Return full content if section not found

        return '\n'.join(section_lines)

    def _call_docs_fetch_command(self, library_name: str, version: str = None, url: str = None, format_option: str = None) -> bool:
        """Call the existing docs:fetch command for a single library."""
        try:
            cmd = ['python3', '.claude/commands/_lib/scripts/docs-fetch.py', library_name]

            if version:
                cmd.extend(['--version', version])
            if url:
                cmd.extend(['--url', url])
            if format_option:
                cmd.extend(['--format', format_option])

            # Run the command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                logger.info(f"✅ Successfully fetched documentation for {library_name}")
                return True
            else:
                logger.error(f"❌ Failed to fetch documentation for {library_name}: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error(f"❌ Timeout fetching documentation for {library_name}")
            return False
        except Exception as e:
            logger.error(f"❌ Error fetching documentation for {library_name}: {str(e)}")
            return False

    def fetch_batch_documentation(self, markdown_content: str, **options) -> bool:
        """Main method to fetch documentation for multiple libraries from markdown."""
        try:
            logger.info("Starting batch documentation fetch...")

            # Extract libraries from markdown
            libraries = self.parser.extract_libraries_from_markdown(markdown_content)

            if not libraries:
                print("❌ No libraries found in markdown content")
                print("Make sure your markdown contains bullet points with links like:")
                print("* [Library Name](https://example.com) - Description")
                return False

            print(f"\n📚 Found {len(libraries)} libraries to process:")
            for lib in libraries:
                version_info = f" (v{lib['version']})" if lib['version'] else ""
                print(f"  • {lib['display_name']}{version_info} → {lib['mapped_name']}")

            # Check for dry run
            if options.get('dry-run', False):
                print(f"\n🔍 Dry run completed - would fetch {len(libraries)} libraries")
                return True

            # Process libraries
            successful = []
            failed = []
            skipped = []

            if options.get('parallel', False):
                successful, failed, skipped = self._process_libraries_parallel(libraries, options)
            else:
                successful, failed, skipped = self._process_libraries_sequential(libraries, options)

            # Report results
            self._report_results(successful, failed, skipped, len(libraries))

            # Update CLAUDE.md with batch results if there were successes
            if successful:
                self._update_claude_md_batch(successful)

            return len(successful) > 0

        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
            return False

    def _process_libraries_sequential(self, libraries: List[Dict], options: Dict) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Process libraries sequentially."""
        successful = []
        failed = []
        skipped = []

        for i, lib in enumerate(libraries, 1):
            print(f"\n[{i}/{len(libraries)}] Processing {lib['display_name']}...")

            # Check if should skip existing
            if options.get('skip-existing', False) and self._documentation_exists(lib['mapped_name']):
                print(f"  ⏭️  Skipping {lib['mapped_name']} - documentation already exists")
                skipped.append(lib)
                continue

            # Fetch documentation
            success = self._call_docs_fetch_command(
                lib['mapped_name'],
                lib['version'],
                lib['url'],
                options.get('format')
            )

            if success:
                successful.append(lib)
            else:
                failed.append(lib)

        return successful, failed, skipped

    def _process_libraries_parallel(self, libraries: List[Dict], options: Dict, max_workers: int = 3) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """Process libraries in parallel."""
        successful = []
        failed = []
        skipped = []

        # Filter out libraries to skip
        to_process = []
        for lib in libraries:
            if options.get('skip-existing', False) and self._documentation_exists(lib['mapped_name']):
                print(f"  ⏭️  Skipping {lib['mapped_name']} - documentation already exists")
                skipped.append(lib)
            else:
                to_process.append(lib)

        if not to_process:
            return successful, failed, skipped

        print(f"\n🔄 Processing {len(to_process)} libraries in parallel (max {max_workers} workers)...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_lib = {
                executor.submit(
                    self._call_docs_fetch_command,
                    lib['mapped_name'],
                    lib['version'],
                    lib['url'],
                    options.get('format')
                ): lib for lib in to_process
            }

            # Process completed tasks
            for future in as_completed(future_to_lib):
                lib = future_to_lib[future]
                try:
                    success = future.result()
                    if success:
                        successful.append(lib)
                        print(f"  ✅ Completed {lib['mapped_name']}")
                    else:
                        failed.append(lib)
                        print(f"  ❌ Failed {lib['mapped_name']}")
                except Exception as e:
                    failed.append(lib)
                    print(f"  ❌ Exception for {lib['mapped_name']}: {str(e)}")

        return successful, failed, skipped

    def _documentation_exists(self, library_name: str) -> bool:
        """Check if documentation already exists for a library."""
        base_dir = Path('/workspace/docs')

        # Check in all possible directories
        for lib_type in ['frameworks', 'libraries', 'languages']:
            lib_dir = base_dir / lib_type / library_name.lower()
            if lib_dir.exists() and (lib_dir / 'index.md').exists():
                return True

        return False

    def _report_results(self, successful: List[Dict], failed: List[Dict], skipped: List[Dict], total: int):
        """Report the results of batch processing."""
        print(f"\n" + "="*60)
        print(f"📊 BATCH PROCESSING COMPLETE")
        print(f"="*60)
        print(f"Total libraries processed: {total}")
        print(f"✅ Successful: {len(successful)}")
        print(f"❌ Failed: {len(failed)}")
        print(f"⏭️  Skipped: {len(skipped)}")
        print(f"Success rate: {(len(successful)/(total-len(skipped))*100):.1f}%" if total-len(skipped) > 0 else "N/A")

        if successful:
            print(f"\n✅ Successfully processed:")
            for lib in successful:
                version_info = f" (v{lib['version']})" if lib['version'] else ""
                print(f"  • {lib['display_name']}{version_info}")

        if failed:
            print(f"\n❌ Failed to process:")
            for lib in failed:
                version_info = f" (v{lib['version']})" if lib['version'] else ""
                print(f"  • {lib['display_name']}{version_info}")

        if skipped:
            print(f"\n⏭️  Skipped (already exists):")
            for lib in skipped:
                version_info = f" (v{lib['version']})" if lib['version'] else ""
                print(f"  • {lib['display_name']}{version_info}")

    def _update_claude_md_batch(self, successful_libraries: List[Dict]):
        """Update CLAUDE.md with batch results."""
        try:
            print(f"\n📝 Updating CLAUDE.md with {len(successful_libraries)} new documentation references...")
            # The individual docs-fetch calls should have already updated CLAUDE.md
            # This is a placeholder for any batch-specific updates
            logger.info(f"CLAUDE.md should be updated by individual docs-fetch calls")
        except Exception as e:
            logger.error(f"Error updating CLAUDE.md: {str(e)}")

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python docs-fetch-batch.py '<markdown_content>' [options]")
        print("   or: python docs-fetch-batch.py --file README.md [options]")
        print("")
        print("Options:")
        print("  --dry-run       Show what would be fetched without actually fetching")
        print("  --parallel      Process libraries in parallel (faster)")
        print("  --skip-existing Skip libraries that already have documentation")
        print("  --update        Update existing documentation")
        print("  --format FORMAT Output format (full, minimal, api-only)")
        print("  --file PATH     Read markdown from file")
        print("  --section NAME  Extract specific section from file")
        print("")
        print("Example:")
        print("  python docs-fetch-batch.py '* [React](https://reactjs.org) - UI library'")
        print("  python docs-fetch-batch.py --file README.md --section 'Dependencies'")
        sys.exit(1)

    # Parse arguments
    args_string = ' '.join(sys.argv[1:])
    fetcher = BatchDocsFetcher()

    try:
        markdown_content, options = fetcher.parse_arguments(args_string)
        success = fetcher.fetch_batch_documentation(markdown_content, **options)

        if success:
            print(f"\n🎉 Batch documentation fetch completed successfully!")
            sys.exit(0)
        else:
            print(f"\n💥 Batch documentation fetch failed!")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()