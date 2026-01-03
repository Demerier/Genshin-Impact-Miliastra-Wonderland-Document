#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复格式质量问题，为缺少标题的文件添加标题
"""

import os
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s')
logger = logging.getLogger(__name__)

def fix_missing_titles(markdown_dir: str):
    """为缺少标题的文件添加标题"""
    # 定义需要修复的文件列表（根据AI自检报告）
    files_to_fix = [
        "其它概念.md",
        "外围系统.md",
        "客户端节点.md",
        "服务器节点.md",
        "概念介绍.md",
        "界面介绍.md",
        "节点介绍.md",
        "节点图高级特性.md",
        "资产.md",
        "资源系统.md",
        "辅助功能.md",
        "附录.md",
        "高级概念.md"
    ]
    
    fixed_count = 0
    
    for filename in files_to_fix:
        file_path = os.path.join(markdown_dir, filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在: {file_path}")
            continue
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有标题
        if content.startswith('# '):
            logger.info(f"文件已有标题: {filename}")
            continue
        
        # 提取文件名作为标题（不含扩展名）
        title = os.path.splitext(filename)[0]
        
        # 添加标题到文件开头
        new_content = f"# {title}\n\n{content}"
        
        # 写入修复后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logger.info(f"已为文件添加标题: {filename}")
        fixed_count += 1
    
    logger.info(f"格式修复完成，共修复 {fixed_count} 个文件")

def main():
    """主函数"""
    # 获取Markdown文件目录
    markdown_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'markdown')
    
    logger.info(f"开始修复格式问题，目标目录: {markdown_dir}")
    
    # 修复缺少标题的文件
    fix_missing_titles(markdown_dir)
    
    logger.info("所有格式修复任务已完成")

if __name__ == "__main__":
    main()
