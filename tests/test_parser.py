import pytest
from bs4 import BeautifulSoup
from src.crawler.parser import Parser


class TestParser:
    """测试页面内容解析器"""
    
    def setup_method(self):
        """初始化测试环境"""
        self.parser = Parser()
    
    def test_parse_content_with_doc_view(self):
        """测试使用.doc-view选择器解析内容"""
        html = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <div class="doc-view">
                <h1>Test Title</h1>
                <p>This is a test paragraph.</p>
            </div>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser.parse_content(soup)
        
        assert result is not None
        assert result['title'] == 'Test Page'
        assert '# Test Title' in result['content']
        assert 'This is a test paragraph.' in result['content']
    
    def test_parse_content_with_content_class(self):
        """测试使用.content选择器解析内容"""
        html = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <div class="content">
                <h1>Test Title</h1>
                <p>This is a test paragraph.</p>
            </div>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser.parse_content(soup)
        
        assert result is not None
        assert result['title'] == 'Test Page'
        assert '# Test Title' in result['content']
        assert 'This is a test paragraph.' in result['content']
    
    def test_parse_content_with_main_tag(self):
        """测试使用main标签解析内容"""
        html = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <main>
                <h1>Test Title</h1>
                <p>This is a test paragraph.</p>
            </main>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser.parse_content(soup)
        
        assert result is not None
        assert result['title'] == 'Test Page'
        assert '# Test Title' in result['content']
        assert 'This is a test paragraph.' in result['content']
    
    def test_parse_content_with_body_tag(self):
        """测试使用body标签解析内容"""
        html = '''
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Title</h1>
            <p>This is a test paragraph.</p>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        result = self.parser.parse_content(soup)
        
        assert result is not None
        assert result['title'] == 'Test Page'
        assert '# Test Title' in result['content']
        assert 'This is a test paragraph.' in result['content']
    
    def test_parse_links(self):
        """测试解析页面中的链接"""
        html = '''
        <html>
        <body>
            <a href="https://act.mihoyo.com/ys/ugc/tutorial/detail/test1">Link 1</a>
            <a href="https://act.mihoyo.com/ys/ugc/tutorial/detail/test2">Link 2</a>
            <a href="https://example.com">External Link</a>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0'
        links = self.parser.parse_links(soup, base_url)
        
        assert len(links) == 2
        assert 'https://act.mihoyo.com/ys/ugc/tutorial/detail/test1' in links
        assert 'https://act.mihoyo.com/ys/ugc/tutorial/detail/test2' in links
    
    def test_parse_images(self):
        """测试解析页面中的图片"""
        html = '''
        <html>
        <body>
            <img src="https://example.com/image1.jpg" alt="Image 1">
            <img src="https://example.com/image2.png" alt="Image 2">
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        images = self.parser.parse_images(soup)
        
        assert len(images) == 2
        assert 'https://example.com/image1.jpg' in images
        assert 'https://example.com/image2.png' in images
    
    def test_parse_links_with_no_matches(self):
        """测试没有匹配链接的情况"""
        html = '''
        <html>
        <body>
            <a href="https://example.com">External Link</a>
            <a href="https://another-example.com">Another External Link</a>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        base_url = 'https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0'
        links = self.parser.parse_links(soup, base_url)
        
        assert len(links) == 0
    
    def test_parse_images_with_no_images(self):
        """测试没有图片的情况"""
        html = '''
        <html>
        <body>
            <h1>Test Title</h1>
            <p>This is a test paragraph with no images.</p>
        </body>
        </html>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        images = self.parser.parse_images(soup)
        
        assert len(images) == 0
