#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
正式爬取启动脚本
用于启动正式爬取任务
"""

import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from crawler import Crawler
from crawl_config import CRAWL_CONFIG, CRAWL_PAGES


def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


def main():
    """主函数"""
    print("=" * 80)
    print("正式爬取启动")
    print("=" * 80)
    print()

    # 显示配置信息
    print("【爬取配置】")
    print(f"  页面数量: {len(CRAWL_PAGES)}")
    print(f"  请求延迟: {CRAWL_CONFIG.request_delay_min}-{CRAWL_CONFIG.request_delay_max}秒")
    print(f"  最大重试: {CRAWL_CONFIG.max_retries}次")
    print(f"  超时时间: {CRAWL_CONFIG.timeout}秒")
    print(f"  增量更新: {CRAWL_CONFIG.enable_incremental}")
    print(f"  断点续传: {CRAWL_CONFIG.enable_resume}")
    print()

    # 显示页面列表
    print("【爬取页面】")
    for i, page in enumerate(CRAWL_PAGES, 1):
        print(f"  {i}. {page.name}")
        print(f"     URL: {page.url}")
        print(f"     描述: {page.description}")
        print()

    # 显示存储路径
    print("【存储路径】")
    print(f"  Markdown目录: {CRAWL_CONFIG.markdown_dir}")
    print(f"  HTML目录: {CRAWL_CONFIG.html_dir}")
    print(f"  图片目录: {CRAWL_CONFIG.images_dir}")
    print(f"  日志目录: {CRAWL_CONFIG.log_dir}")
    print()

    # 开始爬取
    print("=" * 80)
    print("开始爬取...")
    print("=" * 80)
    print()

    # 创建并启动爬取器
    crawler = Crawler(config=CRAWL_CONFIG)
    crawler.crawl(CRAWL_PAGES)

    print()
    print("=" * 80)
    print("正式爬取完成")
    print("=" * 80)


if __name__ == "__main__":
    setup_logging()
    main()
