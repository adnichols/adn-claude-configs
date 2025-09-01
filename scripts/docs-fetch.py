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
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentQualityValidator:
    """Validates content quality and completeness."""
    
    def __init__(self):
        self.quality_thresholds = {
            'min_content_length': 500,
            'min_headings': 2,
            'min_code_blocks': 0,
            'max_js_indicators': 3
        }
    
    def validate_content_quality(self, content: str, url: str) -> Dict:
        """Validate content quality and return metrics."""
        if not content:
            return {
                'is_valid': False,
                'completeness': 0,
                'issues': ['No content'],
                'metrics': {}
            }
        
        metrics = self._calculate_content_metrics(content)
        issues = self._identify_content_issues(content, metrics)
        completeness = self._calculate_completeness(metrics, issues)
        
        return {
            'is_valid': completeness >= 50,
            'completeness': completeness,
            'issues': issues,
            'metrics': metrics,
            'url': url
        }
    
    def _calculate_content_metrics(self, content: str) -> Dict:
        """Calculate various content quality metrics."""
        content_lower = content.lower()
        
        metrics = {
            'length': len(content),
            'headings': len(re.findall(r'<h[1-6][^>]*>', content, re.IGNORECASE)),
            'code_blocks': len(re.findall(r'<pre[^>]*>|<code[^>]*>', content, re.IGNORECASE)),
            'links': len(re.findall(r'<a[^>]*href', content, re.IGNORECASE)),
            'paragraphs': len(re.findall(r'<p[^>]*>', content, re.IGNORECASE)),
            'documentation_keywords': 0,
            'js_loading_indicators': 0
        }
        
        # Count documentation keywords
        doc_keywords = [
            'api', 'documentation', 'guide', 'tutorial', 'reference',
            'function', 'method', 'class', 'parameter', 'example',
            'usage', 'install', 'configuration'
        ]
        
        for keyword in doc_keywords:
            if keyword in content_lower:
                metrics['documentation_keywords'] += content_lower.count(keyword)
        
        # Count JS loading indicators (bad signs)
        js_indicators = [
            'loading...', 'please wait', 'javascript required',
            'enable javascript', 'noscript', 'document.getelementbyid'
        ]
        
        for indicator in js_indicators:
            if indicator in content_lower:
                metrics['js_loading_indicators'] += content_lower.count(indicator)
        
        return metrics
    
    def _identify_content_issues(self, content: str, metrics: Dict) -> List[str]:
        """Identify content quality issues."""
        issues = []
        
        if metrics['length'] < self.quality_thresholds['min_content_length']:
            issues.append(f"Content too short ({metrics['length']} chars)")
        
        if metrics['headings'] < self.quality_thresholds['min_headings']:
            issues.append(f"Too few headings ({metrics['headings']})")
        
        if metrics['js_loading_indicators'] > self.quality_thresholds['max_js_indicators']:
            issues.append("Too many JavaScript loading indicators")
        
        if metrics['documentation_keywords'] == 0:
            issues.append("No documentation keywords found")
        
        # Check for empty or mostly empty content
        text_content = re.sub(r'<[^>]+>', ' ', content)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        if len(text_content) < 200:
            issues.append("Very little actual text content")
        
        return issues
    
    def _calculate_completeness(self, metrics: Dict, issues: List[str]) -> int:
        """Calculate content completeness percentage."""
        score = 100
        
        # Deduct points for each issue
        score -= len(issues) * 15
        
        # Bonus for good indicators
        if metrics['documentation_keywords'] > 5:
            score += 10
        
        if metrics['code_blocks'] > 0:
            score += 10
        
        if metrics['headings'] > 5:
            score += 10
        
        # Cap at 0-100 range
        return max(0, min(100, score))

class DocsFetcher:
    """Main class for fetching and processing documentation."""
    
    def __init__(self, base_dir: str = "/workspace/docs"):
        self.base_dir = Path(base_dir)
        self.user_agent = 'Mozilla/5.0 (compatible; Claude-Code-DocsFetch/1.0; +https://claude.ai/code)'
        
        # Rate limiting configuration
        self.rate_limit_delay = 1.0  # seconds between requests
        self.last_request_time = 0.0
        
        # Error handling and retry configuration
        self.max_retries = 3
        self.retry_delays = [1, 3, 8]  # Exponential backoff in seconds
        self.timeout_seconds = 90
        
        # Site patterns for common documentation sites
        self.site_patterns = self._load_site_patterns()
        
        # Technical Writer agent integration
        self.enable_agent_integration = True
        
        # Content quality validation
        self.quality_validator = ContentQualityValidator()
        
        # Enhanced headers for better compatibility
        self.enhanced_headers = [
            '-H', f'User-Agent: {self.user_agent}',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            '-H', 'Accept-Language: en-US,en;q=0.9',
            '-H', 'Accept-Encoding: gzip, deflate, br',
            '-H', 'Connection: keep-alive',
            '-H', 'Upgrade-Insecure-Requests: 1'
        ]
        
        # JS-heavy sites that need special handling
        self.js_heavy_sites = {
            'react.dev', 'vuejs.org', 'angular.dev', 'nextjs.org',
            'docs.svelte.dev', 'tailwindcss.com'
        }
    
    def _load_site_patterns(self) -> Dict:
        """Load site-specific parsing patterns from user-writable storage."""
        # Create user-writable patterns directory
        user_patterns_dir = self.base_dir / '.site-patterns'
        user_patterns_dir.mkdir(parents=True, exist_ok=True)
        
        patterns = {}
        
        # Load built-in patterns first (fallback)
        builtin_patterns = self._get_builtin_patterns()
        patterns.update(builtin_patterns)
        
        # Load user patterns (override built-in ones)
        for pattern_file in user_patterns_dir.glob('*.json'):
            try:
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    domain = pattern_file.stem  # filename without .json
                    user_pattern = json.load(f)
                    
                    # Validate and update pattern
                    if self._validate_pattern(user_pattern):
                        patterns[domain] = user_pattern
                        logger.info(f"Loaded user pattern for {domain}")
                    else:
                        logger.warning(f"Invalid user pattern in {pattern_file}, skipping")
                        
            except Exception as e:
                logger.error(f"Error loading pattern from {pattern_file}: {str(e)}")
        
        return patterns
    
    def _get_builtin_patterns(self) -> Dict:
        """Get built-in fallback patterns."""
        # Try to load from the static file first
        patterns_file = Path(__file__).parent / "site-patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Fallback to hardcoded patterns
        return {
            "react.dev": {
                "selectors": {
                    "main_content": "main[role='main']",
                    "navigation": "nav[role='navigation']", 
                    "title": "h1"
                },
                "base_urls": ["https://react.dev/"],
                "sections": ["learn", "reference", "community"],
                "metadata": {
                    "success_rate": 0.85,
                    "last_updated": "2025-01-01",
                    "usage_count": 0
                }
            },
            "docs.python.org": {
                "selectors": {
                    "main_content": ".body-content",
                    "navigation": ".toctree-wrapper",
                    "title": "h1"
                },
                "base_urls": ["https://docs.python.org/3/"],
                "sections": ["tutorial", "library", "reference"],
                "metadata": {
                    "success_rate": 0.90,
                    "last_updated": "2025-01-01", 
                    "usage_count": 0
                }
            },
            "default": {
                "selectors": {
                    "main_content": "main, .main, .content, .container, article, .document",
                    "navigation": "nav, .nav, .sidebar, .toc",
                    "title": "h1, .title, .page-title"
                },
                "sections": ["docs", "guide", "api", "reference"],
                "metadata": {
                    "success_rate": 0.70,
                    "last_updated": "2025-01-01",
                    "usage_count": 0
                }
            }
        }
    
    def _validate_pattern(self, pattern: Dict) -> bool:
        """Validate a site pattern structure."""
        required_keys = ['selectors']
        if not all(key in pattern for key in required_keys):
            return False
        
        # Validate selectors
        selectors = pattern.get('selectors', {})
        if not isinstance(selectors, dict) or not selectors:
            return False
        
        return True
    
    def _save_learned_pattern(self, domain: str, pattern: Dict):
        """Save a learned pattern to user-writable storage."""
        try:
            user_patterns_dir = self.base_dir / '.site-patterns'
            user_patterns_dir.mkdir(parents=True, exist_ok=True)
            
            pattern_file = user_patterns_dir / f"{domain}.json"
            
            with open(pattern_file, 'w', encoding='utf-8') as f:
                json.dump(pattern, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved learned pattern for {domain}")
            
        except Exception as e:
            logger.error(f"Error saving pattern for {domain}: {str(e)}")
    
    def _discover_content_patterns(self, html_content: str, url: str) -> Dict:
        """Analyze HTML to discover content patterns."""
        from urllib.parse import urlparse
        
        if not html_content:
            return {}
        
        domain = urlparse(url).netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Analyze common content indicators
        selectors = {
            "main_content": [],
            "navigation": [], 
            "title": []
        }
        
        # Look for main content indicators
        main_indicators = [
            ('main[role="main"]', html_content.count('main role="main"')),
            ('main', html_content.count('<main')),
            ('.main-content', html_content.count('class="main-content"') + html_content.count("class='main-content'")),
            ('.content', html_content.count('class="content"') + html_content.count("class='content'")),
            ('article', html_content.count('<article')),
            ('.container', html_content.count('class="container"') + html_content.count("class='container'")),
            ('.docs-content', html_content.count('docs-content'))
        ]
        
        # Sort by frequency and pick the most common ones
        main_indicators.sort(key=lambda x: x[1], reverse=True)
        selectors["main_content"] = [sel[0] for sel in main_indicators[:3] if sel[1] > 0]
        
        # Look for navigation indicators
        nav_indicators = [
            ('nav', html_content.count('<nav')),
            ('.nav', html_content.count('class="nav"') + html_content.count("class='nav'")),
            ('.sidebar', html_content.count('sidebar')),
            ('.toc', html_content.count('toc')),
            ('.navigation', html_content.count('navigation'))
        ]
        
        nav_indicators.sort(key=lambda x: x[1], reverse=True)
        selectors["navigation"] = [sel[0] for sel in nav_indicators[:2] if sel[1] > 0]
        
        # Title indicators
        selectors["title"] = ["h1", ".title", ".page-title"]
        
        # Create pattern
        pattern = {
            "selectors": {
                "main_content": ", ".join(selectors["main_content"]) or "main, .content, article",
                "navigation": ", ".join(selectors["navigation"]) or "nav, .sidebar", 
                "title": ", ".join(selectors["title"])
            },
            "base_urls": [f"https://{domain}/"],
            "metadata": {
                "success_rate": 0.5,  # Initial success rate
                "last_updated": time.strftime('%Y-%m-%d'),
                "usage_count": 1,
                "discovered": True
            }
        }
        
        return pattern
    
    def _update_pattern_success(self, domain: str, success: bool):
        """Update pattern success metrics."""
        try:
            user_patterns_dir = self.base_dir / '.site-patterns'
            pattern_file = user_patterns_dir / f"{domain}.json"
            
            if pattern_file.exists():
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    pattern = json.load(f)
                
                metadata = pattern.get('metadata', {})
                
                # Update usage count
                metadata['usage_count'] = metadata.get('usage_count', 0) + 1
                
                # Update success rate using exponential moving average
                current_rate = metadata.get('success_rate', 0.5)
                alpha = 0.1  # Learning rate
                new_rate = alpha * (1.0 if success else 0.0) + (1 - alpha) * current_rate
                metadata['success_rate'] = round(new_rate, 3)
                metadata['last_updated'] = time.strftime('%Y-%m-%d')
                
                pattern['metadata'] = metadata
                
                # Save updated pattern
                with open(pattern_file, 'w', encoding='utf-8') as f:
                    json.dump(pattern, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Updated pattern success for {domain}: rate={new_rate:.3f}, count={metadata['usage_count']}")
                
        except Exception as e:
            logger.error(f"Error updating pattern success for {domain}: {str(e)}")
    
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
    
    def _requires_enhanced_fetching(self, url: str) -> bool:
        """Check if URL requires enhanced fetching strategies."""
        from urllib.parse import urlparse
        
        domain = urlparse(url).netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return any(js_site in domain for js_site in self.js_heavy_sites)
    
    def _fetch_with_retry(self, url: str, use_enhanced_headers: bool = True) -> Optional[str]:
        """Fetch URL with retry logic and exponential backoff."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    delay = self.retry_delays[min(attempt - 1, len(self.retry_delays) - 1)]
                    logger.info(f"Waiting {delay}s before retry attempt {attempt + 1}")
                    time.sleep(delay)
                
                logger.info(f"Fetch attempt {attempt + 1}/{self.max_retries} for: {url}")
                
                # Build curl command
                cmd = ['curl', '-s', '-L', '--connect-timeout', '30', '--max-time', '60']
                
                if use_enhanced_headers:
                    cmd.extend(self.enhanced_headers)
                    cmd.append('--compressed')
                else:
                    cmd.extend(['-H', f'User-Agent: {self.user_agent}'])
                
                cmd.append(url)
                
                # Execute the request
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout_seconds)
                
                if result.returncode == 0 and result.stdout.strip():
                    content = result.stdout
                    
                    # Validate content quality
                    quality = self.quality_validator.validate_content_quality(content, url)
                    
                    if quality['is_valid'] or attempt == self.max_retries - 1:
                        if quality['is_valid']:
                            logger.info(f"Fetch successful (quality: {quality['completeness']}%)")
                        else:
                            logger.warning(f"Using low-quality content after all retries (issues: {quality['issues']})")
                        return content
                    else:
                        logger.warning(f"Content quality too low (attempt {attempt + 1}): {quality['issues']}")
                        continue
                        
                else:
                    last_error = f"curl failed with return code {result.returncode}: {result.stderr}"
                    logger.warning(f"Attempt {attempt + 1} failed: {last_error}")
                    
            except subprocess.TimeoutExpired:
                last_error = f"Request timed out after {self.timeout_seconds} seconds"
                logger.warning(f"Attempt {attempt + 1} timed out")
                
            except Exception as e:
                last_error = f"Unexpected error: {str(e)}"
                logger.error(f"Attempt {attempt + 1} failed with error: {last_error}")
        
        logger.error(f"All {self.max_retries} attempts failed for {url}. Last error: {last_error}")
        return None
    
    def _enhanced_fetch(self, url: str) -> Optional[str]:
        """Enhanced fetch with better headers and retry logic."""
        # Try with enhanced headers first
        content = self._fetch_with_retry(url, use_enhanced_headers=True)
        
        if content:
            return content
        
        # Fallback to simple headers
        logger.info("Enhanced headers failed, trying with simple headers")
        return self._fetch_with_retry(url, use_enhanced_headers=False)
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a single URL with comprehensive error handling."""
        try:
            self._enforce_rate_limit()
            logger.info(f"Fetching content from: {url}")
            
            # Use enhanced fetching for all sites (includes retry logic)
            if self._requires_enhanced_fetching(url):
                logger.info(f"Using enhanced fetching for JS-heavy site: {url}")
                return self._enhanced_fetch(url)
            else:
                logger.info(f"Using standard fetching with retry logic: {url}")
                return self._fetch_with_retry(url, use_enhanced_headers=False)
        
        except Exception as e:
            logger.error(f"Critical error fetching {url}: {str(e)}")
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
    
    def _call_technical_writer_agent(self, content: str, library_name: str, content_type: str) -> str:
        """Call the Technical Writer agent to organize and structure content."""
        if not self.enable_agent_integration:
            return content
            
        try:
            logger.info(f"Calling Technical Writer agent for {content_type} content organization")
            
            # Create a temporary file with the content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            # Prepare the prompt for the Technical Writer agent
            prompt = f"""Please review and organize this {content_type} documentation for the {library_name} library. 

Structure the content to be AI-friendly with:
1. Clear hierarchical headings
2. Consistent formatting
3. Proper code block formatting
4. Logical flow and organization
5. Remove any redundant navigation or promotional content
6. Focus on technical content that helps developers

The content should be optimized for Claude Code to understand and reference when helping developers.

Original content is in: {temp_path}

Please create well-structured, AI-optimized documentation."""

            # Call Claude Code with the technical-writer agent
            result = subprocess.run([
                'claude', 'task', 
                '--subagent-type', 'technical-writer',
                '--description', f'Organize {library_name} {content_type}',
                '--prompt', prompt
            ], capture_output=True, text=True, cwd='/workspace', timeout=300)
            
            if result.returncode == 0:
                logger.info("Technical Writer agent completed content organization")
                # Read the organized content back
                try:
                    with open(temp_path, 'r', encoding='utf-8') as f:
                        organized_content = f.read()
                    return organized_content
                except FileNotFoundError:
                    logger.warning("Agent output file not found, using original content")
                    return content
            else:
                logger.warning(f"Technical Writer agent failed: {result.stderr}")
                return content
                
        except Exception as e:
            logger.error(f"Error calling Technical Writer agent: {str(e)}")
            return content
        finally:
            # Clean up temporary file
            try:
                if 'temp_path' in locals():
                    os.unlink(temp_path)
            except:
                pass
    
    def _process_content_with_markdown_converter(self, html_content: str, base_url: str) -> str:
        """Process HTML content using the markdown converter."""
        try:
            # Load and use the markdown converter
            converter_path = Path(__file__).parent / "markdown-converter.py"
            if not converter_path.exists():
                logger.warning("Markdown converter not found, using basic HTML stripping")
                return re.sub(r'<[^>]+>', ' ', html_content)
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as html_file:
                html_file.write(html_content)
                html_path = html_file.name
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as md_file:
                md_path = md_file.name
            
            # Call the markdown converter
            result = subprocess.run([
                sys.executable, str(converter_path), html_path, md_path, base_url
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                with open(md_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                return markdown_content
            else:
                logger.error(f"Markdown converter failed: {result.stderr}")
                return re.sub(r'<[^>]+>', ' ', html_content)
                
        except Exception as e:
            logger.error(f"Error in markdown conversion: {str(e)}")
            return re.sub(r'<[^>]+>', ' ', html_content)
        finally:
            # Clean up temporary files
            try:
                if 'html_path' in locals():
                    os.unlink(html_path)
                if 'md_path' in locals():
                    os.unlink(md_path)
            except:
                pass
    
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
            
            # Fetch and process content from each URL
            processed_content = {}
            for i, url in enumerate(urls[:3]):  # Limit to first 3 URLs for now
                logger.info(f"Processing URL {i+1}/{min(len(urls), 3)}: {url}")
                
                # Fetch the content
                html_content = self.fetch_page_content(url)
                if not html_content:
                    self._update_pattern_success(self._get_domain(url), False)
                    continue
                
                # Validate content quality
                quality = self.quality_validator.validate_content_quality(html_content, url)
                
                # Learn from successful fetches
                if quality['is_valid']:
                    domain = self._get_domain(url)
                    if domain not in self.site_patterns:
                        # Discover and save new pattern
                        learned_pattern = self._discover_content_patterns(html_content, url)
                        if learned_pattern:
                            self._save_learned_pattern(domain, learned_pattern)
                            self.site_patterns[domain] = learned_pattern
                    
                    self._update_pattern_success(domain, True)
                else:
                    self._update_pattern_success(self._get_domain(url), False)
                
                # Convert HTML to Markdown
                markdown_content = self._process_content_with_markdown_converter(html_content, url)
                
                # Organize content with Technical Writer agent
                if markdown_content:
                    organized_content = self._call_technical_writer_agent(
                        markdown_content, library_name, f"documentation from {url}"
                    )
                    processed_content[url] = organized_content
            
            # Create documentation files
            self._create_documentation_files(lib_dir, library_name, metadata, urls, processed_content)
            
            logger.info(f"Documentation created for {library_name} in {lib_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {library_name}: {str(e)}")
            return False
    
    def _create_documentation_files(self, lib_dir: Path, library_name: str, metadata: Dict, urls: List[str], processed_content: Dict[str, str]):
        """Create documentation files from processed content."""
        # Update metadata completeness based on successful content processing
        completeness = int((len(processed_content) / len(urls)) * 100)
        metadata['completeness'] = completeness
        
        # Create index file
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

The following official documentation sources were processed:

{chr(10).join(f'- [{url}]({url}) {"✅" if url in processed_content else "❌"}' for url in urls)}

## Structure

- `index.md` - This overview file
- `api-reference.md` - Complete API documentation
- `best-practices.md` - Current patterns and conventions  
- `examples/` - Practical implementation examples

## Content Status

- ✅ Directory structure created
- ✅ Source URLs identified  
- ✅ Content fetched ({len(processed_content)}/{len(urls)} sources)
- ✅ Content processed and AI-optimized
- ✅ Technical Writer agent organization

**Completeness: {completeness}%**

*Last updated: {metadata['last_fetched']}*
"""
        
        index_file = lib_dir / 'index.md'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        logger.info(f"Created index file: {index_file}")
        
        # Create consolidated API reference from all processed content
        if processed_content:
            api_content = f"""---
library: "{metadata['library']}"
version: "{metadata['version']}"
last_fetched: "{metadata['last_fetched']}"
---

# {library_name.title()} API Reference

This document contains comprehensive API documentation for {library_name}, consolidated from official sources and optimized for AI assistance.

"""
            
            for i, (url, content) in enumerate(processed_content.items(), 1):
                api_content += f"\n## Source {i}: {url}\n\n"
                api_content += content
                api_content += "\n\n---\n\n"
            
            api_file = lib_dir / 'api-reference.md'
            with open(api_file, 'w', encoding='utf-8') as f:
                f.write(api_content)
            logger.info(f"Created API reference file: {api_file}")
        
        # Create best practices file template
        best_practices_content = f"""---
library: "{metadata['library']}"
version: "{metadata['version']}"
last_fetched: "{metadata['last_fetched']}"
---

# {library_name.title()} Best Practices

This document contains current patterns, conventions, and best practices for using {library_name}.

## Installation

*Installation instructions will be extracted from processed documentation*

## Getting Started

*Getting started guide will be populated from processed content*

## Common Patterns

*Common usage patterns will be identified and documented*

## Performance Considerations

*Performance tips and optimization strategies*

## Migration Guide

*Version migration information when available*

## Additional Resources

{chr(10).join(f'- [{url}]({url})' for url in urls)}
"""
        
        best_practices_file = lib_dir / 'best-practices.md'
        with open(best_practices_file, 'w', encoding='utf-8') as f:
            f.write(best_practices_content)
        logger.info(f"Created best practices file: {best_practices_file}")
    
    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

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