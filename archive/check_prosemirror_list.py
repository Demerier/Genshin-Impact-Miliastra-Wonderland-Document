#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查文档页面中的prosemirror-list-new元素
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_prosemirror_list():
    """检查文档页面中的prosemirror-list-new元素"""
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
            print("=== 查找prosemirror-list-new元素 ===")
            
            # 查找所有prosemirror-list-new元素
            custom_lists = content_div.find_all('div', class_='prosemirror-list-new')
            print(f"找到 {len(custom_lists)} 个prosemirror-list-new元素")
            
            for idx, custom_list in enumerate(custom_lists):
                print(f"\n[{idx}] prosemirror-list-new元素:")
                print(f"  HTML: {custom_list.prettify()[:300]}")
                
                # 查找list-content
                list_content = custom_list.find('div', class_='list-content')
                if list_content:
                    print(f"  list-content文本: '{list_content.get_text(strip=True)}'")
                else:
                    print(f"  警告: 没有找到list-content!")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_prosemirror_list())
