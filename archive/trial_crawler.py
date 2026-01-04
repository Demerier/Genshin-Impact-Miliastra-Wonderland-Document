#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
试行爬取器
基于现有爬虫功能，增强监控和报告能力，用于试行爬取测试
"""

import time
import random
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 本地导入
from trial_crawl_config import TRIAL_CONFIG, TRIAL_PAGES, PARSING_RULES, EXTRACTION_FIELDS
from trial_crawl_monitor import CrawlMonitor, PageMetrics
from src.crawler.parser import Parser
from src.crawler.downloader import Downloader

# 配置日志
def setup_trial_logger(log_dir: str, log_level: str = "DEBUG"):
    """设置试行爬取日志
    
    Args:
        log_dir: 日志目录
        log_level: 日志级别
        
    Returns:
        logger对象
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"trial_crawl_{timestamp}.log"
    
    logger = logging.getLogger("trial_crawler")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


class TrialCrawler:
    """试行爬取器"""
    
    def __init__(self, config=None, monitor=None, logger=None):
        """初始化试行爬取器
        
        Args:
            config: 爬取配置
            monitor: 监控器
            logger: 日志记录器
        """
        self.config = config or TRIAL_CONFIG
        self.monitor = monitor or CrawlMonitor(output_dir=self.config.log_dir)
        self.logger = logger or setup_trial_logger(self.config.log_dir, self.config.log_level)
        
        # 初始化解析器和下载器
        self.parser = Parser(images_dir=self.config.images_dir)
        self.downloader = Downloader()
        
        # 创建必要的目录
        Path(self.config.markdown_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.html_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.images_dir).mkdir(parents=True, exist_ok=True)
        
        self.logger.info("试行爬取器初始化完成")
        self.logger.info(f"配置: 请求延迟 {self.config.request_delay_min}-{self.config.request_delay_max}秒, "
                        f"最大重试 {self.config.max_retries}次, 超时 {self.config.timeout}秒")
    
    def crawl_single_page(self, page_url: str, page_name: str, retry_count: int = 0) -> Optional[Dict[str, Any]]:
        """爬取单个页面
        
        Args:
            page_url: 页面URL
            page_name: 页面名称
            retry_count: 当前重试次数
            
        Returns:
            爬取结果字典
        """
        from playwright.sync_api import sync_playwright
        from bs4 import BeautifulSoup
        
        # 开始监控
        metrics = self.monitor.start_page(page_url, page_name)
        
        try:
            self.logger.info(f"开始爬取页面: {page_name} ({page_url})")
            self.logger.info(f"重试次数: {retry_count}/{self.config.max_retries}")
            
            # 使用Playwright获取页面
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                # 创建页面
                page = browser.new_page()
                
                # 设置请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                for key, value in headers.items():
                    page.set_extra_http_headers({key: value})
                
                # 记录开始时间
                start_time = time.time()
                
                # 导航到页面
                try:
                    page.goto(
                        page_url,
                        wait_until=self.config.wait_until,
                        timeout=self.config.wait_timeout
                    )
                    
                    # 额外等待确保DOM更新完成
                    page.wait_for_timeout(self.config.additional_wait)
                    
                    # 计算加载时间
                    load_time = time.time() - start_time
                    
                    # 获取页面内容
                    html = page.content()
                    status_code = 200
                    
                    self.logger.info(f"页面加载成功: {page_name}, 加载时间: {load_time:.2f}秒")
                    
                except Exception as e:
                    load_time = time.time() - start_time
                    status_code = 0
                    self.logger.error(f"页面加载失败: {page_name}, 错误: {str(e)}")
                    raise
                
                finally:
                    browser.close()
                
                # 解析HTML
                soup = BeautifulSoup(html, 'html.parser')
                
                # 提取数据
                result = self._extract_data(soup, page_url, page_name)
                
                # 更新监控指标
                self.monitor.update_page_content_metrics(
                    title=result.get('title_extracted', False),
                    content=result.get('content_extracted', False),
                    links=result.get('links_extracted', False),
                    images=result.get('images_extracted', False),
                    length=result.get('content_length', 0)
                )
                
                self.monitor.update_page_resource_metrics(
                    image_count=result.get('image_count', 0),
                    images_downloaded=result.get('images_downloaded', 0),
                    link_count=result.get('link_count', 0)
                )
                
                # 保存结果
                if self.config.save_markdown and result.get('content'):
                    self._save_markdown(result, page_url, page_name)
                
                # 标记成功
                self.monitor.end_page(success=True, status_code=status_code, load_time=load_time)
                
                return result
                
        except Exception as e:
            error_message = str(e)
            error_type = type(e).__name__
            
            self.logger.error(f"爬取页面失败: {page_name}, 错误: {error_message}", exc_info=True)
            
            # 记录错误
            self.monitor.record_error(error_message, error_type)
            
            # 重试逻辑
            if retry_count < self.config.max_retries:
                self.monitor.record_retry()
                delay = random.uniform(self.config.request_delay_min, self.config.request_delay_max)
                self.logger.info(f"等待 {delay:.2f}秒后重试...")
                time.sleep(delay)
                return self.crawl_single_page(page_url, page_name, retry_count + 1)
            else:
                # 标记失败
                self.monitor.end_page(success=False)
                return None
    
    def _extract_data(self, soup, url: str, name: str) -> Dict[str, Any]:
        """提取页面数据
        
        Args:
            soup: BeautifulSoup对象
            url: 页面URL
            name: 页面名称
            
        Returns:
            提取的数据字典
        """
        result = {
            'url': url,
            'name': name,
            'title': None,
            'content': None,
            'links': [],
            'images': [],
            'title_extracted': False,
            'content_extracted': False,
            'links_extracted': False,
            'images_extracted': False,
            'content_length': 0,
            'image_count': 0,
            'images_downloaded': 0,
            'link_count': 0
        }
        
        # 设置解析器的页面名称和文档ID，用于生成有意义的图片文件名
        self.parser.page_name = name
        
        # 从URL中提取文档ID
        doc_id = None
        if '/detail/' in url:
            doc_id = url.split('/detail/')[-1].split('?')[0]
        self.parser.doc_id = doc_id
        
        # 提取标题
        if self.config.extract_title:
            title = soup.title.string if soup.title else ''
            result['title'] = title
            result['title_extracted'] = bool(title)
            self.logger.debug(f"标题提取: {title[:50] if title else 'None'}...")
        
        # 提取内容
        if self.config.extract_content:
            parsed_data = self.parser.parse_content(soup)
            result['content'] = parsed_data.get('content', '')
            result['content_extracted'] = bool(result['content'])
            result['content_length'] = len(result['content'])
            self.logger.debug(f"内容提取: 长度 {result['content_length']} 字符")
        
        # 提取链接
        if self.config.extract_links:
            links = self.parser.parse_links(soup, url)
            result['links'] = links
            result['link_count'] = len(links)
            result['links_extracted'] = len(links) > 0
            self.logger.debug(f"链接提取: {len(links)} 个链接")
        
        # 提取图片
        if self.config.extract_images:
            images = self.parser.parse_images(soup)
            result['images'] = images
            result['image_count'] = len(images)
            
            # 注意：图片下载已经在parse_content中完成，这里只统计数量
            # 统计已下载的图片数
            downloaded_count = 0
            for img_url in images:
                # 检查图片是否已下载
                local_path = self.parser.download_image(img_url)
                if local_path:
                    downloaded_count += 1
            
            result['images_downloaded'] = downloaded_count
            result['images_extracted'] = len(images) > 0
            self.logger.debug(f"图片提取: {len(images)} 个图片, 下载 {downloaded_count} 个")
        
        return result
    
    def _save_markdown(self, result: Dict[str, Any], url: str, name: str):
        """保存Markdown文件
        
        Args:
            result: 爬取结果
            url: 页面URL
            name: 页面名称
        """
        try:
            # 生成文件名
            from urllib.parse import urlparse
            doc_id = None
            if '/detail/' in url:
                doc_id = url.split('/detail/')[-1].split('?')[0]
            
            filename = f"{name}_{doc_id if doc_id else 'unknown'}.md"
            filepath = Path(self.config.markdown_dir) / filename
            
            # 生成Markdown内容
            content = f"# {result.get('title', name)}\n\n"
            content += f"**URL**: {url}\n\n"
            content += f"**爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            content += "---\n\n"
            # 添加页面名称标题
            content += f"## {name}\n\n"
            content += result.get('content', '')
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Markdown文件已保存: {filepath}")
            
        except Exception as e:
            self.logger.error(f"保存Markdown文件失败: {str(e)}", exc_info=True)
    
    def run_trial(self, pages: List = None) -> Dict[str, Any]:
        """运行试行爬取
        
        Args:
            pages: 要爬取的页面列表，默认使用TRIAL_PAGES
            
        Returns:
            爬取结果摘要
        """
        if pages is None:
            pages = TRIAL_PAGES
        
        self.logger.info(f"开始试行爬取，共 {len(pages)} 个页面")
        self.monitor.start_crawl()
        
        results = []
        
        for i, page in enumerate(pages, 1):
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"爬取进度: {i}/{len(pages)}")
            self.logger.info(f"{'='*60}")
            
            # 爬取页面
            result = self.crawl_single_page(page.url, page.name)
            
            if result:
                results.append(result)
            
            # 请求延迟（最后一个页面不需要延迟）
            if i < len(pages):
                delay = random.uniform(self.config.request_delay_min, self.config.request_delay_max)
                self.logger.info(f"等待 {delay:.2f}秒后继续...")
                time.sleep(delay)
        
        self.monitor.end_crawl()
        
        # 保存指标
        metrics_file = self.monitor.save_metrics()
        
        # 打印摘要
        self.monitor.print_summary()
        
        self.logger.info(f"试行爬取完成，指标已保存到: {metrics_file}")
        
        return self.monitor.get_summary()
    
    def generate_report(self) -> str:
        """生成试行爬取报告
        
        Returns:
            报告文件路径
        """
        from trial_crawl_report import TrialCrawlReportGenerator
        
        report_generator = TrialCrawlReportGenerator(
            monitor=self.monitor,
            config=self.config,
            logger=self.logger
        )
        
        report_file = report_generator.generate_report()
        
        self.logger.info(f"试行爬取报告已生成: {report_file}")
        
        return report_file
