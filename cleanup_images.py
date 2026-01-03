#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
清理旧的图片文件
"""

import os
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def cleanup_images(directory: str):
    """
    清理指定目录中的所有图片文件
    
    Args:
        directory: 图片目录路径
    """
    try:
        logger.info(f"开始清理图片目录: {directory}")
        
        # 检查目录是否存在
        if not os.path.exists(directory):
            logger.error(f"目录不存在: {directory}")
            return
        
        # 获取目录中的所有文件
        files = os.listdir(directory)
        logger.info(f"找到 {len(files)} 个文件")
        
        # 删除所有PNG图片文件
        deleted = 0
        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(directory, file)
                try:
                    os.remove(file_path)
                    deleted += 1
                    logger.info(f"删除文件: {file}")
                except Exception as e:
                    logger.error(f"删除文件失败 {file}: {e}")
        
        logger.info(f"清理完成，共删除 {deleted} 个PNG图片文件")
        
    except Exception as e:
        logger.error(f"清理图片目录失败: {e}", exc_info=True)

if __name__ == "__main__":
    images_dir = "data/images"
    cleanup_images(images_dir)
