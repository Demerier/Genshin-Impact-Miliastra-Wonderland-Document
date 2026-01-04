#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
清理试行爬取的图片文件
"""

import os
import glob
from pathlib import Path

# 清理图片目录
images_dir = Path("data/images_trial")

if images_dir.exists():
    # 删除所有图片文件
    image_files = list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg")) + list(images_dir.glob("*.jpeg"))
    
    for image_file in image_files:
        try:
            os.remove(image_file)
            print(f"已删除: {image_file}")
        except Exception as e:
            print(f"删除失败 {image_file}: {e}")
    
    print(f"清理完成，共删除 {len(image_files)} 个图片文件")
else:
    print(f"图片目录不存在: {images_dir}")
