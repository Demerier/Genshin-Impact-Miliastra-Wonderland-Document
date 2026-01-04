#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
爬虫运行入口脚本
用于测试爬取少量页面
"""

import os
import sys
import hashlib
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crawler.spider import Spider
from config import logger

def get_url_hash(url):
    """获取URL的哈希值，用于生成唯一文件名"""
    hasher = hashlib.md5()
    hasher.update(url.encode('utf-8'))
    return hasher.hexdigest()[:8]

def main():
    """主函数"""
    logger.info("开始运行爬虫测试")
    
    # 创建Spider实例，设置最大深度为0，只爬取起始页面，不跟随任何链接
    spider = Spider(max_depth=0)
    
    # 选择少量页面进行测试爬取
    # 这里使用米哈游文档页面作为测试
    test_urls = [
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/3181125d733050e5c2a8a04da7e204dd"
    ]
    
    # 创建html目录用于保存原始HTML
    html_dir = Path("data/html")
    html_dir.mkdir(parents=True, exist_ok=True)
    
    for url in test_urls:
        logger.info(f"开始爬取测试页面: {url}")
        try:
            # 保存原始HTML内容
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until="networkidle")
                html_content = page.content()
                browser.close()
                
                # 保存HTML到文件
                url_hash = get_url_hash(url)
                html_file_path = html_dir / f"test_page_{url_hash}.html"
                with open(html_file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                logger.info(f"已保存原始HTML到: {html_file_path}")
            
            # 正常爬取
            visited_urls = spider.crawl(url)
            logger.info(f"爬取完成，共访问 {len(visited_urls)} 个页面")
        except Exception as e:
            logger.error(f"爬取页面失败 {url}: {e}", exc_info=True)
    
    logger.info("爬虫测试运行结束")

if __name__ == "__main__":
    main()
