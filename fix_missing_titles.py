#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复缺少标题的Markdown文件
"""

import os
import re

def fix_missing_titles():
    """修复缺少标题的Markdown文件"""
    
    # 定义数据目录
    markdown_dir = os.path.join('data', 'markdown')
    
    # 获取所有Markdown文件
    all_files = os.listdir(markdown_dir)
    markdown_files = [f for f in all_files if f.endswith('.md')]
    
    print(f"开始修复缺少标题的Markdown文件...")
    print(f"总共有 {len(markdown_files)} 个Markdown文件")
    
    # 统计修复的文件数量
    fixed_count = 0
    
    # 遍历所有Markdown文件
    for filename in markdown_files:
        file_path = os.path.join(markdown_dir, filename)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有标题（以#开头的行）
        has_title = bool(re.search(r'^#', content, re.MULTILINE))
        
        if not has_title:
            # 从文件名提取标题，去除文档ID后缀
            # 例如："其它概念_mhh5zgir.md" -> "其它概念"
            title = filename.split('_')[0].replace('.md', '')
            
            # 生成修复后的内容
            fixed_content = f"# {title}\n\n{content}"
            
            # 保存修复后的内容
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"修复了文件: {filename}")
            fixed_count += 1
    
    print(f"\n修复完成，共修复了 {fixed_count} 个文件")
    
    return fixed_count

if __name__ == '__main__':
    fix_missing_titles()
