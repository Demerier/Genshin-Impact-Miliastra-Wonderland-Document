#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查文档页面中的空内容
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_empty_content():
    """检查文档页面中的空内容"""
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
            print("=== 检查内容区域的前几个元素 ===")
            
            # 获取内容区域的前10个子元素
            children = list(content_div.children)
            for idx, child in enumerate(children[:10]):
                if hasattr(child, 'name'):
                    print(f"\n[{idx}] 标签: {child.name}")
                    print(f"  class: {child.get('class')}")
                    print(f"  文本: {child.get_text(strip=True)[:100]}")
                    print(f"  HTML: {str(child)[:200]}")
                else:
                    print(f"\n[{idx}] 文本节点: '{str(child)[:100]}'")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_empty_content())
