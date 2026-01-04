#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
找出缺少的文档
"""

import os
import json
from collections import Counter

def find_missing_documents():
    """找出缺少的文档"""
    
    # 文件路径
    url_list_file = os.path.join('data', 'url_list.txt')
    doc_id_map_file = os.path.join('data', 'doc_id_map.json')
    markdown_dir = os.path.join('data', 'markdown')
    
    # 读取URL列表
    with open(url_list_file, 'r', encoding='utf-8') as f:
        url_list = [line.strip() for line in f if line.strip()]
    
    print(f"URL列表包含 {len(url_list)} 个URL")
    
    # 读取文档ID映射表
    with open(doc_id_map_file, 'r', encoding='utf-8') as f:
        doc_id_map = json.load(f)
    
    # 检查重复的标题
    print("\n检查重复标题:")
    title_list = []
    for url in url_list:
        doc_id = url.split('/')[-1]
        title = doc_id_map.get(doc_id, doc_id)
        title_list.append(title)
    
    # 统计标题出现次数
    title_counter = Counter(title_list)
    duplicate_titles = {title: count for title, count in title_counter.items() if count > 1}
    
    if duplicate_titles:
        print(f"发现 {len(duplicate_titles)} 个重复标题:")
        for title, count in duplicate_titles.items():
            print(f"  - {title}: 出现 {count} 次")
        
        # 显示重复标题对应的文档ID和URL
        print("\n重复标题对应的文档ID和URL:")
        for title, count in duplicate_titles.items():
            print(f"\n  标题: {title}")
            for url in url_list:
                doc_id = url.split('/')[-1]
                if doc_id_map.get(doc_id, doc_id) == title:
                    print(f"    - ID: {doc_id}, URL: {url}")
    else:
        print("没有发现重复标题")
    
    # 获取实际生成的Markdown文件名
    generated_files = os.listdir(markdown_dir)
    generated_titles = [f.replace('.md', '') for f in generated_files if f.endswith('.md')]
    
    print(f"\n实际生成了 {len(generated_titles)} 个Markdown文件")
    
    # 检查实际文件与预期文件的差异
    expected_set = set(title_list)
    generated_set = set(generated_titles)
    
    print(f"\n预期标题数量: {len(expected_set)}")
    print(f"实际标题数量: {len(generated_set)}")
    
    # 找出缺少的标题
    missing_titles = expected_set - generated_set
    print(f"\n缺少的标题数量: {len(missing_titles)}")
    if missing_titles:
        print("缺少的标题:")
        for title in missing_titles:
            print(f"  - {title}")
    
    # 找出多余的标题（可能是旧文件）
    extra_titles = generated_set - expected_set
    print(f"\n多余的标题数量: {len(extra_titles)}")
    if extra_titles:
        print("多余的标题:")
        for title in extra_titles:
            print(f"  - {title}")
    
    # 详细检查每个URL对应的文档是否生成
    print("\n详细检查结果:")
    missing_docs = []
    
    for i, url in enumerate(url_list, 1):
        doc_id = url.split('/')[-1]
        title = doc_id_map.get(doc_id, doc_id)
        filename = f"{title}.md"
        file_path = os.path.join(markdown_dir, filename)
        
        if os.path.exists(file_path):
            status = "✓ 已生成"
        else:
            status = "✗ 缺失"
            missing_docs.append((i, doc_id, title, url))
        
        print(f"{i:3d}. ID: {doc_id}, 标题: {title}, 状态: {status}")
    
    print(f"\n缺少的文档数量: {len(missing_docs)}")
    print("缺少的文档详细信息:")
    for i, doc_id, title, url in missing_docs:
        print(f"  {i:3d}. ID: {doc_id}, 标题: {title}, URL: {url}")
    
    return missing_docs

if __name__ == '__main__':
    find_missing_documents()

