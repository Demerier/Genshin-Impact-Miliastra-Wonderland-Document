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
    
    # 定义起始URL和保存目录
    start_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
    markdown_save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'markdown')
    images_save_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'images')
    
    # 确保保存目录存在
    os.makedirs(markdown_save_dir, exist_ok=True)
    os.makedirs(images_save_dir, exist_ok=True)
    
    try:
        # 获取起始页面内容
        logger.info(f"Crawling start page: {start_url}")
        page_content = spider.get_page(start_url)
        
        if page_content:
            # 解析页面内容
            parsed_content = parser.parse_content(page_content)
            if parsed_content:
                logger.info(f"Successfully parsed content from {start_url}")
                
                # 解析页面中的链接
                links = parser.parse_links(page_content, start_url)
                logger.info(f"Found {len(links)} links on the page")
                
                # 解析页面中的图片
                images = parser.parse_images(page_content)
                logger.info(f"Found {len(images)} images on the page")
                
                # 保存Markdown文件
                title = parsed_content['title'] or 'index'
                filename = downloader.save_markdown(parsed_content['content'], title, markdown_save_dir)
                logger.info(f"Saved Markdown file: {filename}")
                
                # 下载图片
                for img_url in images:
                    downloaded_filename = downloader.download_image(img_url, images_save_dir)
                    if downloaded_filename:
                        logger.info(f"Downloaded image: {downloaded_filename}")
                    else:
                        logger.warning(f"Failed to download image: {img_url}")
                
                # 爬取链接页面（示例：只爬取前5个链接作为测试）
                logger.info("Crawling linked pages...")
                for i, link in enumerate(links[:5]):
                    logger.info(f"Crawling page {i+1}/{5}: {link}")
                    linked_page = spider.get_page(link)
                    if linked_page:
                        linked_content = parser.parse_content(linked_page)
                        if linked_content:
                            linked_title = linked_content['title'] or f'page-{i+1}'
                            linked_filename = downloader.save_markdown(linked_content['content'], linked_title, markdown_save_dir)
                            logger.info(f"Saved linked page: {linked_filename}")
                            
                            # 下载链接页面中的图片
                            linked_images = parser.parse_images(linked_page)
                            for img_url in linked_images:
                                downloaded_filename = downloader.download_image(img_url, images_save_dir)
                                if downloaded_filename:
                                    logger.info(f"Downloaded image from linked page: {downloaded_filename}")
                                else:
                                    logger.warning(f"Failed to download image from linked page: {img_url}")
                    else:
                        logger.warning(f"Failed to get linked page: {link}")
        else:
            logger.error(f"Failed to get start page: {start_url}")
    
    except Exception as e:
        logger.error(f"An error occurred during crawl: {str(e)}", exc_info=True)
    
    logger.info("Crawl process completed.")


if __name__ == "__main__":
    main()
