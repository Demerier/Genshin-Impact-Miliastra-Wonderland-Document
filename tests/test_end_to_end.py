#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
端到端测试用例
验证整个爬取流程的完整性
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.crawler.spider import Spider
from src.crawler.parser import Parser

class TestEndToEnd(unittest.TestCase):
    """端到端测试"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.images_dir = os.path.join(self.temp_dir.name, "images")
        os.makedirs(self.images_dir, exist_ok=True)
        
        # 创建测试用的HTML内容
        self.test_html = """
        <html>
        <head>
            <title>测试页面</title>
        </head>
        <body>
            <div class='doc-view'>
                <h1>测试页面</h1>
                <p>这是一个测试页面，用于验证端到端爬取流程。</p>
                <img src='https://example.com/test-image1.png' alt='测试图片1'>
                <img src='https://example.com/test-image2.png' alt='测试图片2'>
                <a href='https://act.mihoyo.com/ys/ugc/tutorial/detail/test1'>相关链接</a>
            </div>
        </body>
        </html>
        """
    
    def tearDown(self):
        """清理测试环境"""
        self.temp_dir.cleanup()
    
    @patch('src.crawler.spider.sync_playwright')
    @patch.object(Parser, 'download_image')
    def test_full_crawl_process(self, mock_download_image, mock_playwright):
        """测试完整的爬取流程"""
        # 模拟Playwright的返回值
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.content.return_value = self.test_html
        mock_browser.new_page.return_value = mock_page
        mock_playwright_context = MagicMock()
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_context
        
        # 模拟图片下载返回值
        mock_download_image.side_effect = [
            os.path.join(self.images_dir, "image1.png"),
            os.path.join(self.images_dir, "image2.png")
        ]
        
        # 创建Spider和Parser实例
        spider = Spider(max_depth=1)
        parser = Parser(images_dir=self.images_dir)
        
        # 测试爬取单个页面
        url = "https://example.com/test-page"
        visited_urls = spider.crawl(url)
        
        # 验证爬取结果
        self.assertIsInstance(visited_urls, list)
        self.assertEqual(len(visited_urls), 1)
        self.assertIn(url, visited_urls)
        
        # 测试解析器功能
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(self.test_html, 'html.parser')
        parsed_result = parser.parse_content(soup)
        
        # 验证解析结果
        self.assertIsInstance(parsed_result, dict)
        self.assertIn('title', parsed_result)
        self.assertIn('content', parsed_result)
        self.assertEqual(parsed_result['title'], "测试页面")
        
        # 验证Markdown内容包含图片链接
        self.assertIn("image1.png", parsed_result['content'])
        self.assertIn("image2.png", parsed_result['content'])
        
        # 验证图片下载方法被调用
        self.assertEqual(mock_download_image.call_count, 2)
    
    @patch('src.crawler.spider.sync_playwright')
    @patch.object(Parser, 'download_image')
    def test_crawl_with_depth(self, mock_download_image, mock_playwright):
        """测试带深度控制的爬取"""
        # 模拟Playwright的返回值
        mock_browser = MagicMock()
        
        # 模拟第一级页面
        page1_html = """
        <html>
        <head>
            <title>页面1</title>
        </head>
        <body>
            <div class='doc-view'>
                <h1>页面1</h1>
                <p>这是第一级页面，包含一个链接到第二级页面。</p>
                <a href='https://example.com/page2'>页面2</a>
            </div>
        </body>
        </html>
        """
        
        # 模拟第二级页面
        page2_html = """
        <html>
        <head>
            <title>页面2</title>
        </head>
        <body>
            <div class='doc-view'>
                <h1>页面2</h1>
                <p>这是第二级页面，包含一个链接到第三级页面。</p>
                <a href='https://example.com/page3'>页面3</a>
            </div>
        </body>
        </html>
        """
        
        # 模拟第三级页面
        page3_html = """
        <html>
        <head>
            <title>页面3</title>
        </head>
        <body>
            <div class='doc-view'>
                <h1>页面3</h1>
                <p>这是第三级页面。</p>
            </div>
        </body>
        </html>
        """
        
        # 设置mock_page的content方法根据URL返回不同的HTML内容
        mock_page = MagicMock()
        mock_page.content.side_effect = [page1_html, page2_html]
        mock_browser.new_page.return_value = mock_page
        mock_playwright_context = MagicMock()
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_context
        
        # 模拟图片下载返回值
        mock_download_image.return_value = os.path.join(self.images_dir, "test.png")
        
        # 创建Spider实例，设置最大深度为1
        spider = Spider(max_depth=1)
        
        # 测试爬取，最大深度为1
        start_url = "https://example.com/page1"
        visited_urls = spider.crawl(start_url)
        
        # 验证爬取结果，应该只爬取2个页面（页面1和页面2）
        self.assertEqual(len(visited_urls), 2)
        self.assertIn("https://example.com/page1", visited_urls)
        self.assertIn("https://example.com/page2", visited_urls)
        self.assertNotIn("https://example.com/page3", visited_urls)

if __name__ == '__main__':
    unittest.main()