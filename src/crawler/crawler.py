#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
正式爬取器
基于试行爬取器，用于正式爬取目标网站
"""

import time
import random
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 本地导入
from crawl_config import CRAWL_CONFIG, CRAWL_PAGES, PARSING_RULES, EXTRACTION_FIELDS
from src.crawler.parser import Parser
from src.crawler.downloader import Downloader

# 配置日志
def setup_crawl_logger(log_dir: str, log_level: str = "INFO"):
    """设置爬取日志

    Args:
        log_dir: 日志目录
        log_level: 日志级别

    Returns:
        logger对象
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"crawl_{timestamp}.log"

    logger = logging.getLogger("crawl")
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


class Crawler:
    """正式爬取器"""

    def __init__(self, config=None, logger=None):
        """初始化爬取器

        Args:
            config: 爬取配置
            logger: 日志记录器
        """
        self.config = config or CRAWL_CONFIG
        self.logger = logger or setup_crawl_logger(self.config.log_dir, self.config.log_level)

        # 初始化解析器和下载器
        self.parser = Parser(images_dir=self.config.images_dir)
        self.downloader = Downloader()

        # 创建必要的目录
        Path(self.config.markdown_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.html_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.images_dir).mkdir(parents=True, exist_ok=True)
        Path(self.config.log_dir).mkdir(parents=True, exist_ok=True)

        # 加载断点续传信息
        self.resume_data = self._load_resume_data()

        # 统计信息
        self.stats = {
            'total_pages': 0,
            'successful_pages': 0,
            'failed_pages': 0,
            'skipped_pages': 0,
            'total_load_time': 0,
            'total_content_length': 0,
            'total_images_downloaded': 0,
            'total_links_extracted': 0,
            'total_retries': 0,
            'total_errors': 0
        }

        self.logger.info("爬取器初始化完成")
        self.logger.info(f"配置: 请求延迟 {self.config.request_delay_min}-{self.config.request_delay_max}秒, "
                        f"最大重试 {self.config.max_retries}次, 超时 {self.config.timeout}秒")
        self.logger.info(f"增量更新: {self.config.enable_incremental}, "
                        f"跳过已存在: {self.config.skip_existing}, "
                        f"断点续传: {self.config.enable_resume}")

    def _load_resume_data(self):
        """加载断点续传数据

        Returns:
            断点续传数据字典
        """
        if not self.config.enable_resume:
            return {}

        resume_file = Path(self.config.resume_file)
        if not resume_file.exists():
            return {}

        try:
            with open(resume_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"加载断点续传数据: {len(data.get('completed', []))} 个已完成页面")
            return data
        except Exception as e:
            self.logger.warning(f"加载断点续传数据失败: {e}")
            return {}

    def _save_resume_data(self):
        """保存断点续传数据"""
        if not self.config.enable_resume:
            return

        try:
            resume_file = Path(self.config.resume_file)
            resume_file.parent.mkdir(parents=True, exist_ok=True)

            data = {
                'completed': self.resume_data.get('completed', []),
                'failed': self.resume_data.get('failed', []),
                'timestamp': datetime.now().isoformat()
            }

            with open(resume_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            self.logger.debug(f"保存断点续传数据: {len(data['completed'])} 个已完成页面")
        except Exception as e:
            self.logger.warning(f"保存断点续传数据失败: {e}")

    def crawl_single_page(self, page_url: str, page_name: str, retry_count: int = 0) -> Optional[Dict[str, Any]]:
        """爬取单个页面

        Args:
            page_url: 页面URL
            page_name: 页面名称
            retry_count: 当前重试次数

        Returns:
            爬取结果字典
        """
        self.logger.info(f"开始爬取页面: {page_name} ({page_url})")
        self.logger.info(f"重试次数: {retry_count}/{self.config.max_retries}")

        # 检查是否已爬取
        if self.config.enable_incremental and self.config.skip_existing:
            if page_url in self.resume_data.get('completed', []):
                self.logger.info(f"页面已爬取，跳过: {page_name}")
                self.stats['skipped_pages'] += 1
                return None

        try:
            # 使用Playwright获取页面
            from playwright.sync_api import sync_playwright
            from bs4 import BeautifulSoup
            
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
                
                # 导航到页面
                start_time = time.time()
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
                html_content = page.content()
                status_code = 200
                
                browser.close()

            self.logger.info(f"页面加载成功: {page_name}, 加载时间: {load_time:.2f}秒")

            # 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # 提取数据
            result = self._extract_data(soup, page_url, page_name)

            # 添加加载时间和状态码
            result['load_time'] = load_time
            result['status_code'] = status_code

            # 保存Markdown文件
            if self.config.save_markdown and result['content']:
                self._save_markdown(page_url, page_name, result['content'])

            # 保存HTML文件
            if self.config.save_html:
                self._save_html(page_url, page_name, html_content)

            # 更新统计信息
            self.stats['total_pages'] += 1
            self.stats['successful_pages'] += 1
            self.stats['total_load_time'] += load_time
            self.stats['total_content_length'] += result.get('content_length', 0)
            self.stats['total_images_downloaded'] += result.get('images_downloaded', 0)
            self.stats['total_links_extracted'] += result.get('link_count', 0)

            # 更新断点续传数据
            if self.config.enable_resume:
                if 'completed' not in self.resume_data:
                    self.resume_data['completed'] = []
                self.resume_data['completed'].append(page_url)
                self._save_resume_data()

            self.logger.info(f"页面爬取成功: {page_name} (状态码: {status_code}, 加载时间: {load_time:.2f}秒)")

            return result

        except Exception as e:
            self.logger.error(f"爬取页面失败: {page_name}, 错误: {e}", exc_info=True)

            # 更新统计信息
            self.stats['total_pages'] += 1
            self.stats['failed_pages'] += 1
            self.stats['total_retries'] += retry_count
            self.stats['total_errors'] += 1

            # 更新断点续传数据
            if self.config.enable_resume:
                if 'failed' not in self.resume_data:
                    self.resume_data['failed'] = []
                self.resume_data['failed'].append({
                    'url': page_url,
                    'name': page_name,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
                self._save_resume_data()

            # 重试逻辑
            if retry_count < self.config.max_retries:
                wait_time = random.uniform(
                    self.config.request_delay_min,
                    self.config.request_delay_max
                )
                self.logger.info(f"等待 {wait_time:.2f}秒后重试...")
                time.sleep(wait_time)
                return self.crawl_single_page(page_url, page_name, retry_count + 1)
            else:
                self.logger.error(f"达到最大重试次数，放弃爬取: {page_name}")
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
            links = self.parser.parse_links(soup, base_url=url)
            result['links'] = links
            result['links_extracted'] = bool(links)
            result['link_count'] = len(links)
            self.logger.debug(f"链接提取: {result['link_count']} 个链接")

        # 提取图片
        if self.config.extract_images:
            images = self.parser.parse_images(soup)
            result['images'] = images
            result['images_extracted'] = bool(images)
            result['image_count'] = len(images)
            result['images_downloaded'] = 0  # 图片下载在parse_content中处理，这里设置为0
            self.logger.debug(f"图片提取: {result['image_count']} 个图片")

        return result

    def _save_markdown(self, url: str, name: str, content: str):
        """保存Markdown文件

        Args:
            url: 页面URL
            name: 页面名称
            content: Markdown内容
        """
        try:
            # 生成文件名
            doc_id = None
            if '/detail/' in url:
                doc_id = url.split('/detail/')[-1].split('?')[0]

            if doc_id:
                filename = f"{name}_{doc_id}.md"
            else:
                safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{safe_name}.md"

            filepath = Path(self.config.markdown_dir) / filename

            # 构建Markdown内容
            markdown_content = f"# {name}\n\n"
            markdown_content += f"**URL**: {url}\n\n"
            markdown_content += f"**爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            markdown_content += "---\n\n"
            markdown_content += f"## {name}\n\n"
            markdown_content += content

            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            self.logger.info(f"Markdown文件已保存: {filepath}")
        except Exception as e:
            self.logger.error(f"保存Markdown文件失败: {e}", exc_info=True)

    def _save_html(self, url: str, name: str, html_content: str):
        """保存HTML文件

        Args:
            url: 页面URL
            name: 页面名称
            html_content: HTML内容
        """
        try:
            # 生成文件名
            doc_id = None
            if '/detail/' in url:
                doc_id = url.split('/detail/')[-1].split('?')[0]

            if doc_id:
                filename = f"{name}_{doc_id}.html"
            else:
                safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{safe_name}.html"

            filepath = Path(self.config.html_dir) / filename

            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.debug(f"HTML文件已保存: {filepath}")
        except Exception as e:
            self.logger.error(f"保存HTML文件失败: {e}", exc_info=True)

    def crawl(self, pages: List[Any] = None):
        """爬取所有页面

        Args:
            pages: 页面列表，如果为None则使用配置中的页面列表
        """
        if pages is None:
            pages = CRAWL_PAGES

        self.logger.info("=" * 60)
        self.logger.info("开始正式爬取")
        self.logger.info(f"总页面数: {len(pages)}")
        self.logger.info("=" * 60)

        start_time = time.time()

        for i, page in enumerate(pages, 1):
            self.logger.info("=" * 60)
            self.logger.info(f"爬取进度: {i}/{len(pages)}")
            self.logger.info("=" * 60)

            result = self.crawl_single_page(page.url, page.name)

            # 请求延迟
            if i < len(pages):
                wait_time = random.uniform(
                    self.config.request_delay_min,
                    self.config.request_delay_max
                )
                self.logger.info(f"等待 {wait_time:.2f}秒后继续...")
                time.sleep(wait_time)

        total_time = time.time() - start_time

        self.logger.info("=" * 60)
        self.logger.info("爬取结束")
        self.logger.info(f"总耗时: {total_time:.2f}秒")
        self.logger.info("=" * 60)

        # 保存统计信息
        self._save_stats(total_time)

        # 打印摘要报告
        self._print_summary()

    def _save_stats(self, total_time: float):
        """保存统计信息

        Args:
            total_time: 总耗时
        """
        try:
            stats_file = Path(self.config.log_dir) / f"crawl_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            stats = {
                'timestamp': datetime.now().isoformat(),
                'total_time': total_time,
                'stats': self.stats,
                'config': {
                    'request_delay_min': self.config.request_delay_min,
                    'request_delay_max': self.config.request_delay_max,
                    'max_retries': self.config.max_retries,
                    'timeout': self.config.timeout,
                    'enable_incremental': self.config.enable_incremental,
                    'skip_existing': self.config.skip_existing,
                    'enable_resume': self.config.enable_resume
                }
            }

            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

            self.logger.info(f"统计信息已保存: {stats_file}")
        except Exception as e:
            self.logger.error(f"保存统计信息失败: {e}", exc_info=True)

    def _print_summary(self):
        """打印摘要报告"""
        print("\n" + "=" * 80)
        print("正式爬取摘要报告")
        print("=" * 80)

        print("\n【爬取统计】")
        print(f"  总页面数: {self.stats['total_pages']}")
        print(f"  成功页面: {self.stats['successful_pages']}")
        print(f"  失败页面: {self.stats['failed_pages']}")
        print(f"  跳过页面: {self.stats['skipped_pages']}")
        if self.stats['total_pages'] > 0:
            print(f"  成功率: {self.stats['successful_pages'] / self.stats['total_pages'] * 100:.1f}%")
        print(f"  总重试次数: {self.stats['total_retries']}")
        print(f"  总错误次数: {self.stats['total_errors']}")

        print("\n【性能指标】")
        print(f"  总加载时间: {self.stats['total_load_time']:.2f}秒")
        if self.stats['successful_pages'] > 0:
            print(f"  平均加载时间: {self.stats['total_load_time'] / self.stats['successful_pages']:.2f}秒")
        print(f"  总内容长度: {self.stats['total_content_length']}字符")
        if self.stats['successful_pages'] > 0:
            print(f"  平均内容长度: {self.stats['total_content_length'] / self.stats['successful_pages']:.0f}字符")

        print("\n【资源指标】")
        print(f"  下载图片总数: {self.stats['total_images_downloaded']}")
        print(f"  提取链接总数: {self.stats['total_links_extracted']}")
        if self.stats['successful_pages'] > 0:
            print(f"  平均每页图片: {self.stats['total_images_downloaded'] / self.stats['successful_pages']:.1f}")
            print(f"  平均每页链接: {self.stats['total_links_extracted'] / self.stats['successful_pages']:.0f}")

        print("\n" + "=" * 80)


def main():
    """主函数"""
    crawler = Crawler()
    crawler.crawl()


if __name__ == "__main__":
    main()
