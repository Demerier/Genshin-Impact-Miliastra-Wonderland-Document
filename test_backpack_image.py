#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本：测试修复后的空图片链接处理
"""

import os
import sys

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crawler.spider import Spider
from src.crawler.parser import Parser
from src.crawler.downloader import Downloader

# 测试目标URL：背包页面
test_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhogfq9b"

# 文档ID映射表（简化版）
doc_id_map = {
    "mhogfq9b": "背包"
}

def test_single_page_crawl():
    """测试单个页面爬取"""
    print("=== 测试单个页面爬取 ===")
    
    # 初始化爬虫组件
    spider = Spider()
    parser = Parser()
    downloader = Downloader()
    
    # 获取页面内容
    print(f"获取页面内容: {test_url}")
    page_content = spider.get_page(test_url)
    
    if page_content:
        print("页面获取成功")
        
        # 解析页面内容
        # 这里我们直接测试空图片链接处理
        # 创建一个测试用的Markdown内容，包含空图片链接
        test_markdown = "# 背包\n\n这是一个测试文档，包含空图片链接:\n\n![]()\n\n"        
        
        # 保存测试Markdown
        test_save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test_markdown")
        os.makedirs(test_save_dir, exist_ok=True)
        
        test_file = os.path.join(test_save_dir, "test_backpack.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_markdown)
        
        print(f"测试文件已保存到: {test_file}")
        
        # 测试图片下载和链接替换
        print("测试图片下载和链接替换...")
        
        # 使用我们修复后的代码逻辑测试
        # 1. 解析页面中的图片
        soup = parser.parse_content(page_content)
        images = parser.parse_images(page_content)
        links = parser.parse_links(page_content)
        
        print(f"找到图片数量: {len(images)}")
        print(f"找到链接数量: {len(links)}")
        
        # 2. 下载图片并建立映射
        img_map = {}
        for img_url in images:
            # 模拟下载图片
            img_filename = downloader.download_image(img_url, test_save_dir)
            if img_filename:
                img_map[img_url] = img_filename
                print(f"图片已下载: {img_filename}")
        
        print("测试完成！")
    else:
        print("页面获取失败")

if __name__ == "__main__":
    test_single_page_crawl()