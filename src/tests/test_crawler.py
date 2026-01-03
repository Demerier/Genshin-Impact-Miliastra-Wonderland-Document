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
        self.spider = Spider()
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """清理测试环境"""
        self.temp_dir.cleanup()
    
    def test_spider_initialization(self):
        """测试爬虫初始化"""
        self.assertIsInstance(self.spider, Spider)

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
