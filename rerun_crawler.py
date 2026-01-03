#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
重新运行爬虫，生成所有文档
"""

import os
import shutil
import subprocess

def main():
    """主函数"""
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义数据目录
    data_dir = os.path.join(current_dir, "data")
    markdown_dir = os.path.join(data_dir, "markdown")
    
    # 清理现有的Markdown文件
    print(f"清理现有的Markdown文件...")
    if os.path.exists(markdown_dir):
        shutil.rmtree(markdown_dir)
    os.makedirs(markdown_dir, exist_ok=True)
    print(f"Markdown目录已清理: {markdown_dir}")
    
    # 重新运行爬虫
    print(f"\n重新运行爬虫...")
    src_dir = os.path.join(current_dir, "src")
    main_script = os.path.join(src_dir, "main.py")
    
    # 运行主脚本
    subprocess.run(["python", main_script], cwd=current_dir, check=True)
    
    # 统计生成的文件数量
    generated_files = os.listdir(markdown_dir)
    markdown_files = [f for f in generated_files if f.endswith('.md')]
    print(f"\n重新爬取完成，生成了 {len(markdown_files)} 个Markdown文件")

if __name__ == '__main__':
    main()
