#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬虫实现
负责从指定URL获取页面内容，支持动态渲染页面的爬取。
"""

# 标准库导入
import logging
from urllib.parse import urljoin, urlparse

# 第三方库导入
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# 设置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('logs/crawler.log'),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)


class Spider:
    """爬虫类"""

    def __init__(self, headers=None, max_depth=1):
        """初始化爬虫

        Args:
            headers: 请求头
            max_depth: 最大爬取深度
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.max_depth = max_depth
        self.visited_urls = set()

    def get_page(self, url):
        """获取页面内容（支持SPA）

        Args:
            url: 页面URL

        Returns:
            BeautifulSoup对象
        """
        try:
            logger.info(f"开始获取页面: {url}")
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(
                    headless=True,  # 无头模式
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )

                # 创建页面
                page = browser.new_page()

                # 设置请求头
                for key, value in self.headers.items():
                    page.set_extra_http_headers({key: value})

                # 导航到页面，使用更全面的等待条件
                page.goto(url, wait_until='networkidle', timeout=30000)

                # 使用Playwright智能等待，等待页面主要内容加载完成
                # 等待网络空闲后，再等待500ms确保DOM更新完成
                page.wait_for_timeout(500)

                # 获取页面内容
                html = page.content()
                logger.info(f"成功获取页面内容: {url}")

                # 关闭浏览器
                browser.close()

                # 返回BeautifulSoup对象
                return BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logger.error(f"获取页面失败 {url}: {e}", exc_info=True)
            return None

    def crawl(self, start_url):
        """开始爬取

        Args:
            start_url: 起始URL
        """
        logger.info(f"开始爬取，起始URL: {start_url}, 最大深度: {self.max_depth}")
        
        # 初始化爬取队列，格式：(url, depth)
        crawl_queue = [(start_url, 0)]
        
        while crawl_queue:
            current_url, depth = crawl_queue.pop(0)
            
            # 检查是否已访问或超过最大深度
            if current_url in self.visited_urls or depth > self.max_depth:
                continue
            
            # 标记为已访问
            self.visited_urls.add(current_url)
            logger.info(f"正在爬取: {current_url}, 当前深度: {depth}")
            
            # 获取页面内容
            soup = self.get_page(current_url)
            if not soup:
                logger.warning(f"跳过无效页面: {current_url}")
                continue
            
            # TODO: 实现页面内容解析和处理逻辑
            
            # 提取页面中的链接，进行深度爬取
            if depth < self.max_depth:
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    # 转换为绝对URL
                    absolute_url = urljoin(current_url, href)
                    # 检查是否为同一域名下的链接
                    if urlparse(absolute_url).netloc == urlparse(start_url).netloc:
                        crawl_queue.append((absolute_url, depth + 1))
        
        logger.info(f"爬取完成，共访问 {len(self.visited_urls)} 个页面")
        return list(self.visited_urls)
