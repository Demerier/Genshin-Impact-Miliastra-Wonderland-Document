#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试脚本：测试图片下载和命名功能
"""

import os
import sys

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.crawler.downloader import Downloader

def test_image_download():
    """测试图片下载和命名功能"""
    print("=== 测试图片下载和命名功能 ===")
    
    # 初始化下载器
    downloader = Downloader()
    
    # 测试图片URL（模拟CDN链接）
    test_image_urls = [
        "https://example.com/images/backpack123.png",
        "https://example.com/images/item456.jpg",
        "https://example.com/photos/screenshot789.png"
    ]
    
    # 测试保存目录
    test_save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test_images")
    os.makedirs(test_save_dir, exist_ok=True)
    
    # 测试图片下载
    for img_url in test_image_urls:
        print(f"\n测试下载图片: {img_url}")
        try:
            # 下载图片并获取保存的文件名
            filename = downloader.download_image(img_url, test_save_dir)
            if filename:
                print(f"✓ 下载成功")
                print(f"  原始URL: {img_url}")
                print(f"  保存文件名: {filename}")
                print(f"  保存路径: {os.path.join(test_save_dir, filename)}")
                print(f"  文件是否存在: {os.path.exists(os.path.join(test_save_dir, filename))}")
            else:
                print(f"✗ 下载失败")
        except Exception as e:
            print(f"✗ 下载出错: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_image_download()