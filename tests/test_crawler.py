#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬虫功能测试用例
"""

import os
import sys
import unittest
import tempfile
from unittest.mock import MagicMock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.crawler.spider import Spider
from src.crawler.parser import Parser

class TestSpider(unittest.TestCase):
    """测试爬虫功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.spider = Spider(max_depth=1)
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """清理测试环境"""
        self.temp_dir.cleanup()
    
    def test_spider_initialization(self):
        """测试爬虫初始化"""
        self.assertIsInstance(self.spider, Spider)
        self.assertEqual(self.spider.max_depth, 1)
        self.assertEqual(len(self.spider.visited_urls), 0)
    
    @patch('src.crawler.spider.sync_playwright')
    def test_get_page_success(self, mock_playwright):
        """测试成功获取页面"""
        # 模拟Playwright的返回值
        mock_browser = MagicMock()
        mock_page = MagicMock()
        mock_page.content.return_value = "<html><head><title>测试页面</title></head><body><h1>测试页面</h1></body></html>"
        mock_browser.new_page.return_value = mock_page
        mock_playwright_context = MagicMock()
        mock_playwright_context.chromium.launch.return_value = mock_browser
        mock_playwright.return_value.__enter__.return_value = mock_playwright_context
        
        # 调用get_page方法
        url = "https://example.com"
        soup = self.spider.get_page(url)
        
        # 验证结果
        self.assertIsNotNone(soup)
        self.assertEqual(soup.title.string, "测试页面")
    
    @patch('src.crawler.spider.sync_playwright')
    def test_get_page_failure(self, mock_playwright):
        """测试获取页面失败"""
        # 模拟Playwright抛出异常
        mock_playwright.side_effect = Exception("测试异常")
        
        # 调用get_page方法
        url = "https://example.com"
        soup = self.spider.get_page(url)
        
        # 验证结果
        self.assertIsNone(soup)
    
    @patch.object(Spider, 'get_page')
    def test_crawl_single_page(self, mock_get_page):
        """测试爬取单个页面"""
        # 模拟get_page返回值
        from bs4 import BeautifulSoup
        mock_soup = BeautifulSoup("<html><head><title>测试页面</title></head><body><h1>测试页面</h1></body></html>", 'html.parser')
        mock_get_page.return_value = mock_soup
        
        # 调用crawl方法
        start_url = "https://example.com"
        result = self.spider.crawl(start_url)
        
        # 验证结果
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertIn(start_url, result)
        mock_get_page.assert_called_once_with(start_url)
    
    @patch.object(Spider, 'get_page')
    def test_crawl_with_links(self, mock_get_page):
        """测试爬取带有链接的页面"""
        # 模拟get_page返回值，第一次返回带有链接的页面，第二次返回普通页面
        from bs4 import BeautifulSoup
        
        # 第一个页面，带有链接
        page1_html = "<html><head><title>页面1</title></head><body><h1>页面1</h1><a href='/page2'>页面2</a></body></html>"
        mock_soup1 = BeautifulSoup(page1_html, 'html.parser')
        
        # 第二个页面，普通页面
        page2_html = "<html><head><title>页面2</title></head><body><h1>页面2</h1></body></html>"
        mock_soup2 = BeautifulSoup(page2_html, 'html.parser')
        
        # 设置mock的返回值序列
        mock_get_page.side_effect = [mock_soup1, mock_soup2]
        
        # 调用crawl方法
        start_url = "https://example.com"
        result = self.spider.crawl(start_url)
        
        # 验证结果
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIn(start_url, result)
        self.assertIn("https://example.com/page2", result)
        self.assertEqual(mock_get_page.call_count, 2)

class TestParser(unittest.TestCase):
    """测试解析器功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.parser = Parser()
        self.test_html = "<html><head><title>测试页面</title></head><body><h1>测试页面</h1><div class='doc-view'><p>测试内容</p><ul><li>项目1</li><li>项目2</li></ul></div></body></html>"
        # 直接使用BeautifulSoup解析HTML
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup(self.test_html, 'html.parser')
    
    def test_parser_initialization(self):
        """测试解析器初始化"""
        self.assertIsInstance(self.parser, Parser)
    
    def test_parse_content(self):
        """测试内容解析"""
        # 调用解析方法
        result = self.parser.parse_content(self.soup)
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn('title', result)
        self.assertIn('content', result)
        self.assertEqual(result['title'], "测试页面")
        self.assertIn("测试内容", result['content'])
    
    def test_parse_links(self):
        """测试链接解析"""
        # 准备测试数据
        test_html = "<html><body><a href='https://act.mihoyo.com/ys/ugc/tutorial/detail/test1'>链接1</a><a href='https://example.com'>链接2</a></body></html>"
        # 直接使用BeautifulSoup解析HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # 调用解析方法
        links = self.parser.parse_links(soup, "https://act.mihoyo.com")
        
        # 验证结果
        self.assertIsInstance(links, list)
        self.assertEqual(len(links), 1)
        self.assertIn("https://act.mihoyo.com/ys/ugc/tutorial/detail/test1", links)
    
    def test_parse_images(self):
        """测试图片解析"""
        # 准备测试数据
        test_html = "<html><body><img src='https://example.com/image1.jpg' alt='图片1'><img src='https://example.com/image2.jpg' alt='图片2'></body></html>"
        # 直接使用BeautifulSoup解析HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # 调用解析方法
        images = self.parser.parse_images(soup)
        
        # 验证结果
        self.assertIsInstance(images, list)
        self.assertEqual(len(images), 2)
        self.assertIn("https://example.com/image1.jpg", images)
        self.assertIn("https://example.com/image2.jpg", images)

if __name__ == '__main__':
    unittest.main()
