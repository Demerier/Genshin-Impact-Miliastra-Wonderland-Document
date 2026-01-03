#!/usr/bin/env python3
"""
测试爬取脚本
用于验证爬虫是否能够成功爬取页面内容
"""

import os
import sys

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crawler.spider import Spider
from src.crawler.parser import Parser
from src.crawler.downloader import Downloader
from config import logger

# 测试URL
TEST_URL = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
# Markdown保存目录
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
# 图片保存目录
IMAGES_DIR = os.path.join(DATA_DIR, "images")

# 文档ID映射表（用于测试）
doc_id_map = {
    "mh29wpicgvh0": "读前须知"
}

def main():
    """主函数"""
    logger.info("开始测试爬取")
    
    try:
        # 初始化组件
        spider = Spider()
        parser = Parser()
        downloader = Downloader()
        
        # 获取测试页面
        logger.info(f"获取测试页面: {TEST_URL}")
        soup = spider.get_page(TEST_URL)
        
        if soup:
            # 解析页面内容
            logger.info("解析页面内容")
            content_data = parser.parse_content(soup)
            
            # 解析链接
            logger.info("解析页面链接")
            links = parser.parse_links(soup, TEST_URL)
            logger.info(f"提取到 {len(links)} 个链接")
            
            # 解析图片
            logger.info("解析页面图片")
            images = parser.parse_images(soup)
            logger.info(f"提取到 {len(images)} 个图片")
            
            # 保存Markdown文件
            logger.info("保存Markdown文件")
            doc_id = TEST_URL.split('/')[-1]
            title = doc_id_map.get(doc_id, doc_id)
            filename = downloader.save_markdown(content_data['content'], title, MARKDOWN_DIR)
            
            if filename:
                logger.info(f"Markdown文件保存成功: {filename}")
                logger.info("测试爬取成功！")
            else:
                logger.error("Markdown文件保存失败")
                logger.error("测试爬取失败！")
        else:
            logger.error("无法获取测试页面")
            logger.error("测试爬取失败！")
            
    except Exception as e:
        logger.error(f"测试爬取过程中出现错误: {e}")
        logger.error("测试爬取失败！")
        raise

if __name__ == "__main__":
    main()
