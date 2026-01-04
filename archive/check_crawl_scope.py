#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查爬取页面范围
统计并展示所有爬取页面的分类和数量
"""

import sys
sys.path.insert(0, 'c:\\Users\\Demeri\\Documents\\trae_projects\\markdown')

from crawl_config import CRAWL_PAGES


def main():
    """主函数"""
    print("=" * 80)
    print("爬取页面范围检查")
    print("=" * 80)
    print()

    # 按类别统计
    category_stats = {}
    for page in CRAWL_PAGES:
        if page.category not in category_stats:
            category_stats[page.category] = []
        category_stats[page.category].append(page)

    # 显示统计信息
    print("【总体统计】")
    print(f"  总页面数: {len(CRAWL_PAGES)}")
    print(f"  类别数: {len(category_stats)}")
    print()

    # 按优先级统计
    priority_stats = {}
    for page in CRAWL_PAGES:
        if page.priority not in priority_stats:
            priority_stats[page.priority] = []
        priority_stats[page.priority].append(page)

    print("【优先级分布】")
    for priority in sorted(priority_stats.keys()):
        pages = priority_stats[priority]
        print(f"  优先级 {priority}: {len(pages)} 个页面")
    print()

    # 按类别显示详细列表
    print("【分类详情】")
    category_order = ['list', 'basic', 'interface', 'concept', 'node', 'auxiliary', 'appendix']
    category_names = {
        'list': '列表页面',
        'basic': '基础页面',
        'interface': '界面介绍',
        'concept': '概念介绍',
        'node': '节点介绍',
        'auxiliary': '辅助功能',
        'appendix': '附录'
    }

    for category in category_order:
        if category not in category_stats:
            continue
        pages = category_stats[category]
        print(f"\n{category_names.get(category, category)} ({len(pages)} 个页面)")
        print("-" * 80)
        for i, page in enumerate(pages, 1):
            doc_id = page.url.split('/')[-1]
            print(f"  {i}. {page.name}")
            print(f"     文档ID: {doc_id}")
            print(f"     描述: {page.description}")
            print()

    print("=" * 80)
    print("等待确认...")
    print("=" * 80)


if __name__ == "__main__":
    main()
