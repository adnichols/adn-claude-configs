#!/usr/bin/env python3
"""
HTML to Markdown Converter for Claude Code Documentation Fetch
Converts HTML content to AI-friendly Markdown format with proper sanitization.
"""

import re
import html
from pathlib import Path
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

class MarkdownConverter:
    """Converts HTML to AI-friendly Markdown format."""
    
    def __init__(self):
        self.base_url = ""
        
        # HTML tags to Markdown mapping
        self.tag_replacements = {
            'strong': '**{}**',
            'b': '**{}**', 
            'em': '*{}*',
            'i': '*{}*',
            'code': '`{}`',
            'h1': '# {}',
            'h2': '## {}',
            'h3': '### {}',
            'h4': '#### {}',
            'h5': '##### {}',
            'h6': '###### {}',
        }
        
        # Tags that should be removed entirely
        self.remove_tags = {'script', 'style', 'noscript', 'iframe', 'object', 'embed'}
        
        # Block-level elements that need line breaks
        self.block_elements = {'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'blockquote', 'pre'}
    
    def sanitize_html(self, html_content: str) -> str:
        """Sanitize HTML content to prevent script injection."""
        if not html_content:
            return ""
        
        # Remove script tags and their content
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove style tags and their content  
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove potentially dangerous attributes
        dangerous_attrs = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'javascript:']
        for attr in dangerous_attrs:
            html_content = re.sub(rf'{attr}[^>]*', '', html_content, flags=re.IGNORECASE)
        
        # Remove comments
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        return html_content
    
    def extract_text_content(self, html_content: str) -> str:
        """Extract text content from HTML, preserving structure."""
        if not html_content:
            return ""
        
        # Sanitize first
        content = self.sanitize_html(html_content)
        
        # Handle special elements
        content = self._process_code_blocks(content)
        content = self._process_lists(content) 
        content = self._process_links(content)
        content = self._process_images(content)
        content = self._process_tables(content)
        content = self._process_headings(content)
        content = self._process_emphasis(content)
        content = self._process_paragraphs(content)
        
        # Clean up remaining HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        
        # Decode HTML entities
        content = html.unescape(content)
        
        # Clean up whitespace
        content = self._clean_whitespace(content)
        
        return content
    
    def _process_code_blocks(self, content: str) -> str:
        """Process code blocks and inline code."""
        # Handle pre/code blocks (preserve content)
        def replace_pre_code(match):
            code_content = match.group(1)
            # Try to detect language from class attribute
            lang_match = re.search(r'class=["\'](?:language-|lang-|brush:|hljs )([^"\']+)', match.group(0))
            language = lang_match.group(1).split()[0] if lang_match else ''
            
            # Clean the code content but preserve formatting
            code_content = re.sub(r'<[^>]+>', '', code_content)
            code_content = html.unescape(code_content)
            
            return f'\n```{language}\n{code_content.strip()}\n```\n'
        
        # Handle <pre><code> blocks
        content = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', 
                        replace_pre_code, content, flags=re.DOTALL | re.IGNORECASE)
        
        # Handle standalone <pre> blocks
        content = re.sub(r'<pre[^>]*>(.*?)</pre>', 
                        replace_pre_code, content, flags=re.DOTALL | re.IGNORECASE)
        
        # Handle inline code
        content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def _process_lists(self, content: str) -> str:
        """Process ordered and unordered lists."""
        # Process nested lists recursively
        def process_list_items(list_content: str, ordered: bool = False) -> str:
            items = re.findall(r'<li[^>]*>(.*?)</li>', list_content, flags=re.DOTALL | re.IGNORECASE)
            result = []
            
            for i, item in enumerate(items, 1):
                # Clean the item content
                item_text = re.sub(r'<[^>]+>', ' ', item)
                item_text = html.unescape(item_text.strip())
                
                if ordered:
                    result.append(f"{i}. {item_text}")
                else:
                    result.append(f"- {item_text}")
            
            return '\n'.join(result)
        
        # Handle ordered lists
        content = re.sub(r'<ol[^>]*>(.*?)</ol>', 
                        lambda m: '\n' + process_list_items(m.group(1), ordered=True) + '\n',
                        content, flags=re.DOTALL | re.IGNORECASE)
        
        # Handle unordered lists  
        content = re.sub(r'<ul[^>]*>(.*?)</ul>',
                        lambda m: '\n' + process_list_items(m.group(1), ordered=False) + '\n', 
                        content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def _process_links(self, content: str) -> str:
        """Process hyperlinks."""
        def replace_link(match):
            href = match.group(1) if match.group(1) else '#'
            text = match.group(2).strip()
            
            # Handle relative URLs
            if self.base_url and href.startswith('/'):
                href = urljoin(self.base_url, href)
            
            # Skip empty links or anchors
            if not text or href == '#':
                return text
                
            return f'[{text}]({href})'
        
        content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', 
                        replace_link, content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def _process_images(self, content: str) -> str:
        """Process images."""
        def replace_image(match):
            src = match.group(1)
            alt = match.group(2) if match.group(2) else 'Image'
            
            # Handle relative URLs
            if self.base_url and src.startswith('/'):
                src = urljoin(self.base_url, src)
                
            return f'![{alt}]({src})'
        
        content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', 
                        replace_image, content, flags=re.IGNORECASE)
        
        # Handle images without alt text
        content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>', 
                        r'![Image](\1)', content, flags=re.IGNORECASE)
        
        return content
    
    def _process_tables(self, content: str) -> str:
        """Process HTML tables to Markdown format."""
        def process_table(match):
            table_content = match.group(0)
            
            # Extract table rows
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_content, flags=re.DOTALL | re.IGNORECASE)
            if not rows:
                return ""
            
            markdown_rows = []
            is_header = True
            
            for row in rows:
                # Extract cells (th or td)
                cells = re.findall(r'<(?:th|td)[^>]*>(.*?)</(?:th|td)>', row, flags=re.DOTALL | re.IGNORECASE)
                if not cells:
                    continue
                
                # Clean cell content
                clean_cells = []
                for cell in cells:
                    cell_text = re.sub(r'<[^>]+>', ' ', cell)
                    cell_text = html.unescape(cell_text.strip())
                    clean_cells.append(cell_text)
                
                # Create markdown row
                markdown_row = '| ' + ' | '.join(clean_cells) + ' |'
                markdown_rows.append(markdown_row)
                
                # Add header separator after first row
                if is_header and clean_cells:
                    separator = '| ' + ' | '.join(['---'] * len(clean_cells)) + ' |'
                    markdown_rows.append(separator)
                    is_header = False
            
            return '\n' + '\n'.join(markdown_rows) + '\n'
        
        content = re.sub(r'<table[^>]*>.*?</table>', process_table, content, flags=re.DOTALL | re.IGNORECASE)
        return content
    
    def _process_headings(self, content: str) -> str:
        """Process heading tags."""
        for i in range(1, 7):
            pattern = f'<h{i}[^>]*>(.*?)</h{i}>'
            replacement = '#' * i + ' \\1'
            content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def _process_emphasis(self, content: str) -> str:
        """Process emphasis tags (bold, italic)."""
        # Bold tags
        content = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Italic tags
        content = re.sub(r'<(?:em|i)[^>]*>(.*?)</(?:em|i)>', r'*\1*', content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def _process_paragraphs(self, content: str) -> str:
        """Process paragraph tags."""
        # Replace paragraph tags with double line breaks
        content = re.sub(r'<p[^>]*>', '\n\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</p>', '', content, flags=re.IGNORECASE)
        
        # Handle div tags as paragraph breaks
        content = re.sub(r'</?div[^>]*>', '\n', content, flags=re.IGNORECASE)
        
        return content
    
    def _clean_whitespace(self, content: str) -> str:
        """Clean up whitespace and formatting."""
        # Normalize line breaks
        content = re.sub(r'\r\n', '\n', content)
        content = re.sub(r'\r', '\n', content)
        
        # Remove excessive blank lines (more than 2)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Clean up spaces
        content = re.sub(r'[ \t]+', ' ', content)
        
        # Remove trailing whitespace from lines
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        
        # Ensure single space after sentence endings
        content = re.sub(r'([.!?])([A-Z])', r'\1 \2', content)
        
        return content.strip()
    
    def html_to_markdown(self, html_content: str, base_url: str = "") -> str:
        """Convert HTML content to Markdown format."""
        self.base_url = base_url
        
        if not html_content:
            return ""
        
        try:
            markdown_content = self.extract_text_content(html_content)
            return markdown_content
            
        except Exception as e:
            logger.error(f"Error converting HTML to Markdown: {str(e)}")
            # Fallback: just strip tags and clean up
            fallback = re.sub(r'<[^>]+>', ' ', html_content)
            fallback = html.unescape(fallback)
            fallback = self._clean_whitespace(fallback)
            return fallback

def convert_html_file(html_file: Path, output_file: Path, base_url: str = "") -> bool:
    """Convert an HTML file to Markdown."""
    try:
        converter = MarkdownConverter()
        
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        markdown_content = converter.html_to_markdown(html_content, base_url)
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        logger.info(f"Converted {html_file} to {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error converting {html_file}: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python markdown-converter.py <input.html> <output.md> [base_url]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    base_url = sys.argv[3] if len(sys.argv) > 3 else ""
    
    success = convert_html_file(input_file, output_file, base_url)
    sys.exit(0 if success else 1)