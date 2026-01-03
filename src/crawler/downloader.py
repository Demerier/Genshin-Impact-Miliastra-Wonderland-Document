#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
资源下载器
负责将爬取的内容保存为Markdown文件，并下载页面中的图片资源。
"""

# 标准库导入
import os
import hashlib

# 第三方库导入
import requests


class Downloader:
    """资源下载器"""

    def __init__(self, headers=None):
        """初始化下载器

        Args:
            headers: 请求头
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def download_image(self, img_url, save_dir):
        """下载图片

        Args:
            img_url: 图片URL
            save_dir: 保存目录

        Returns:
            保存的文件名
        """
        try:
            # 创建保存目录
            os.makedirs(save_dir, exist_ok=True)

            # 生成文件名 - 使用CDN原始文件名
            # 从URL中提取原始文件名
            original_filename = os.path.basename(img_url).lower()

            # 确保文件名有扩展名
            if '.' not in original_filename:
                # 从URL中提取扩展名
                file_ext = img_url.split('.')[-1].lower()
                # 使用MD5哈希值作为文件名，加上扩展名
                img_hash = hashlib.md5(img_url.encode()).hexdigest()
                filename = f"{img_hash}.{file_ext}"
            else:
                # 使用原始文件名
                filename = original_filename

            save_path = os.path.join(save_dir, filename)

            # 下载图片
            response = requests.get(img_url, headers=self.headers, stream=True)
            response.raise_for_status()

            # 保存图片
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return filename
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image {img_url}: {e}")
            return None

    def save_markdown(self, content, title, save_dir, doc_id=None):
        """保存Markdown文件

        Args:
            content: Markdown内容
            title: 文件名
            save_dir: 保存目录
            doc_id: 文档ID，用于处理重复标题

        Returns:
            保存的文件名
        """
        try:
            # 创建保存目录
            os.makedirs(save_dir, exist_ok=True)

            # 生成文件名，处理重复标题
            if doc_id:
                # 使用文档ID作为后缀，确保文件名唯一
                filename = f"{title}_{doc_id[:8]}.md"
            else:
                filename = f"{title}.md"

            save_path = os.path.join(save_dir, filename)

            # 保存文件
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return filename
        except Exception as e:
            print(f"Error saving Markdown {title}: {e}")
            return None
