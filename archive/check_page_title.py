#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查页面标题结构
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_page_title():
    """检查页面标题结构"""
    url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn4bsi5lb58"
    
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
        
        print("=== 检查页面标题 ===")
        
        # 检查<title>标签
        title = soup.title.string if soup.title else ''
        print(f"页面标题(title标签): {title}")
        
        # 检查内容区域的第一个标题
        content_div = soup.find('div', class_='doc-view')
        if content_div:
            print(f"\n=== 内容区域标题 ===")
            
            # 查找所有标题标签
            for tag in content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                print(f"{tag.name}: {tag.get_text(strip=True)}")
                print(f"  HTML: {tag.prettify()[:200]}")
                print("-" * 60)
            
            # 查找第一个标题元素
            first_heading = content_div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if first_heading:
                print(f"\n第一个标题元素:")
                print(f"  标签: {first_heading.name}")
                print(f"  文本: {first_heading.get_text(strip=True)}")
                print(f"  HTML: {first_heading.prettify()}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_page_title())
