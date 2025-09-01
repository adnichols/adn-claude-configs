#!/usr/bin/env python3
"""
JavaScript Renderer for Claude Code Documentation Fetch
Handles JavaScript-heavy documentation sites with enhanced curl strategies.
"""

import subprocess
import logging
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
from urllib.parse import urlparse, urljoin

logger = logging.getLogger(__name__)

class JavaScriptRenderer:
    """Enhanced fetching for JavaScript-heavy documentation sites using smart curl strategies."""
    
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        
        # Sites that are known to be JavaScript-heavy but often have fallback content
        self.js_heavy_sites = {
            'react.dev', 'vuejs.org', 'angular.dev', 'nextjs.org',
            'docs.svelte.dev', 'tailwindcss.com', 'chakra-ui.com',
            'mui.com', 'ant.design', 'v2.grommet.io'
        }
        
        # Alternative URL patterns for JS-heavy sites that often have static versions
        self.static_alternatives = {
            'react.dev': ['https://reactjs.org/docs/', 'https://legacy.reactjs.org/docs/'],
            'vuejs.org': ['https://v2.vuejs.org/v2/guide/', 'https://vuejs.org/guide/'],
            'angular.dev': ['https://angular.io/docs'],
            'nextjs.org': ['https://nextjs.org/docs']
        }
    
    def _get_enhanced_headers(self) -> List[str]:
        """Get enhanced headers for better JS site compatibility."""
        return [
            '-H', f'User-Agent: {self.user_agent}',
            '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            '-H', 'Accept-Language: en-US,en;q=0.9',
            '-H', 'Accept-Encoding: gzip, deflate, br',
            '-H', 'DNT: 1',
            '-H', 'Connection: keep-alive',
            '-H', 'Upgrade-Insecure-Requests: 1',
            '-H', 'Sec-Fetch-Dest: document',
            '-H', 'Sec-Fetch-Mode: navigate',
            '-H', 'Sec-Fetch-Site: none',
            '-H', 'Sec-Fetch-User: ?1',
            '-H', 'Cache-Control: max-age=0'
        ]
    
    def requires_js_rendering(self, url: str) -> bool:
        """Determine if a URL requires enhanced fetching strategies."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Remove www. prefix for comparison
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Check against known JS-heavy sites
        for js_site in self.js_heavy_sites:
            if js_site in domain:
                return True
        
        # Check for modern documentation site patterns
        modern_patterns = ['.dev/', '.io/', 'docs.', 'api.']
        if any(pattern in domain for pattern in modern_patterns):
            return True
        
        return False
    
    def _try_static_alternatives(self, url: str) -> List[str]:
        """Get alternative static URLs for JS-heavy sites."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if domain.startswith('www.'):
            domain = domain[4:]
        
        alternatives = []
        
        # Check if we have predefined alternatives
        for site, alt_urls in self.static_alternatives.items():
            if site in domain:
                alternatives.extend(alt_urls)
        
        # Try common patterns for static documentation
        base_domain = domain.split('.')[0]
        common_patterns = [
            f"https://docs.{base_domain}.com/",
            f"https://docs.{base_domain}.org/",
            f"https://{base_domain}.readthedocs.io/",
            f"https://github.com/{base_domain}/{base_domain}/tree/main/docs"
        ]
        
        alternatives.extend(common_patterns)
        return alternatives
    
    def _enhanced_curl_fetch(self, url: str) -> Optional[str]:
        """Enhanced curl fetch with better headers and retry logic."""
        try:
            logger.info(f"Enhanced curl fetch for: {url}")
            
            headers = self._get_enhanced_headers()
            
            # First attempt with full headers
            result = subprocess.run([
                'curl', '-s', '-L', '--connect-timeout', '30', '--max-time', '60', '--compressed'
            ] + headers + [url], capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0 and result.stdout.strip():
                # Check if we got meaningful content (not just a JS redirect page)
                content = result.stdout
                if self._is_meaningful_content(content):
                    logger.info("Enhanced curl fetch successful")
                    return content
                else:
                    logger.warning("Got content but it appears to be a JS redirect page")
            
            # Second attempt - try with different approach
            logger.info("Retrying with simplified headers")
            simple_headers = ['-H', f'User-Agent: {self.user_agent}']
            
            result = subprocess.run([
                'curl', '-s', '-L', '--connect-timeout', '30', '--max-time', '60'
            ] + simple_headers + [url], capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
            
            return None
                
        except Exception as e:
            logger.error(f"Error in enhanced curl fetch: {str(e)}")
            return None
    
    def _is_meaningful_content(self, content: str) -> bool:
        """Check if content is meaningful documentation (not just JS loading page)."""
        if not content or len(content) < 500:
            return False
        
        # Look for signs of actual documentation content
        good_indicators = [
            '<h1', '<h2', '<h3', '<pre>', '<code>',
            'documentation', 'API', 'guide', 'tutorial',
            'function', 'method', 'class', 'example'
        ]
        
        # Look for signs of JS-only pages
        bad_indicators = [
            'javascript:void(0)', 'document.createElement',
            'window.location', 'Please enable JavaScript',
            'This site requires JavaScript', 'Loading...',
            'noscript'
        ]
        
        content_lower = content.lower()
        
        good_count = sum(1 for indicator in good_indicators if indicator.lower() in content_lower)
        bad_count = sum(1 for indicator in bad_indicators if indicator.lower() in content_lower)
        
        # Must have some good indicators and not too many bad ones
        return good_count >= 2 and bad_count <= 2
    
    def fetch_js_heavy_page(self, url: str, user_agent: str) -> Optional[str]:
        """Main method to fetch content from JavaScript-heavy pages."""
        logger.info(f"Fetching JavaScript-heavy page: {url}")
        
        # Try enhanced curl first
        content = self._enhanced_curl_fetch(url)
        if content and self._is_meaningful_content(content):
            return content
        
        # Try static alternatives if the original URL failed
        logger.info("Trying static alternatives")
        alternatives = self._try_static_alternatives(url)
        
        for alt_url in alternatives[:3]:  # Try up to 3 alternatives
            logger.info(f"Trying alternative URL: {alt_url}")
            
            # Quick check if URL is accessible
            try:
                check_result = subprocess.run([
                    'curl', '-s', '-I', '--connect-timeout', '10',
                    '-H', f'User-Agent: {user_agent}', alt_url
                ], capture_output=True, text=True, timeout=15)
                
                if check_result.returncode == 0 and '200' in check_result.stdout:
                    alt_content = self._enhanced_curl_fetch(alt_url)
                    if alt_content and self._is_meaningful_content(alt_content):
                        logger.info(f"Successfully fetched from alternative: {alt_url}")
                        return alt_content
            except:
                continue
        
        logger.warning("All fetching methods failed for JavaScript-heavy page")
        return content  # Return whatever we got, even if not ideal
    
def test_js_renderer():
    """Test the JavaScript renderer with a simpler approach."""
    renderer = JavaScriptRenderer()
    test_urls = [
        "https://lodash.com/docs/",
        "https://expressjs.com/"
    ]
    
    for url in test_urls:
        print(f"\nTesting enhanced fetch for: {url}")
        
        if renderer.requires_js_rendering(url):
            print("  -> Requires enhanced fetching")
            content = renderer.fetch_js_heavy_page(url, renderer.user_agent)
        else:
            print("  -> Using standard curl")
            content = renderer._enhanced_curl_fetch(url)
        
        if content:
            print(f"  -> Success: {len(content)} characters")
            meaningful = renderer._is_meaningful_content(content)
            print(f"  -> Meaningful content: {meaningful}")
        else:
            print("  -> Failed to fetch content")

if __name__ == "__main__":
    test_js_renderer()