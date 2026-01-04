#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查页面中实际的列表结构
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_list_structure():
    """检查页面中的列表结构"""
    url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("正在加载页面...")
        await page.goto(url, wait_until="domcontentloaded")
        
        print("等待内容加载...")
        try:
            await page.wait_for_selector('.doc-view', timeout=15000)
        except:
            print("等待.doc-view超时，继续处理...")
        
        await page.wait_for_timeout(5000)
        
        html_content = await page.content()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        content_div = soup.find('div', class_='doc-view')
        
        if content_div:
            print("=== 查找所有prosemirror-list-new元素 ===")
            
            # 查找所有prosemirror-list-new元素
            prosemirror_lists = content_div.find_all('div', class_='prosemirror-list-new')
            print(f"找到 {len(prosemirror_lists)} 个prosemirror-list-new元素")
            
            for i, prosemirror_list in enumerate(prosemirror_lists):
                print(f"\nprosemirror-list-new {i+1}:")
                print(f"  HTML: {prosemirror_list.prettify()[:500]}")
                
                # 检查子元素
                children = list(prosemirror_list.children)
                print(f"  子元素数量: {len(children)}")
                
                for j, child in enumerate(children):
                    if hasattr(child, 'name') and child.name:
                        print(f"    子元素 {j+1}: {child.name}, class: {child.get('class')}")
                        if child.get('class'):
                            print(f"      文本: '{child.get_text(strip=True)[:100]}'")
                    else:
                        print(f"    子元素 {j+1}: 文本节点: '{str(child).strip()[:100]}'")
            
            print("\n=== 查找所有list-content元素 ===")
            
            # 查找所有list-content元素
            list_contents = content_div.find_all('div', class_='list-content')
            print(f"找到 {len(list_contents)} 个list-content元素")
            
            for i, list_content in enumerate(list_contents):
                print(f"\nlist-content {i+1}:")
                print(f"  HTML: {list_content.prettify()[:500]}")
                print(f"  文本: '{list_content.get_text(strip=True)[:100]}'")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_list_structure())
