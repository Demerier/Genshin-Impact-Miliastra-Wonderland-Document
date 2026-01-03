#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
原神千星奇域·综合指南 - 网站爬取主程序
"""

import os
import sys
import logging
from crawler.spider import Spider
from crawler.parser import Parser
from crawler.downloader import Downloader

# 设置日志配置
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'crawl_log.txt')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """主程序入口"""
    logger.info("Starting crawl process...")
    
    # 初始化爬虫组件
    spider = Spider()
    parser = Parser()
    downloader = Downloader()
    
    # TODO: 实现爬取逻辑
    # 示例：爬取指定URL
    # url = "https://example.com"
    # page_content = spider.get_page(url)
    # if page_content:
    #     parsed_content = parser.parse_content(page_content)
    #     links = parser.parse_links(page_content, url)
    #     images = parser.parse_images(page_content, url)
    #     downloader.save_markdown(parsed_content, "example", "data/markdown")
    #     for img_url in images:
    #         downloader.download_image(img_url, "data/images")
    
    logger.info("Crawl process completed.")


if __name__ == "__main__":
    main()
