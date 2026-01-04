#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查页面中的"整体界面"文本
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_page_name():
    """检查页面中的页面名称"""
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
        
        print("=== 查找'整体界面'文本 ===")
        
        # 搜索整个HTML中的"整体界面"
        if '整体界面' in html_content:
            print("找到'整体界面'文本")
            
            # 查找包含"整体界面"的元素
            content_div = soup.find('div', class_='doc-view')
            if content_div:
                for element in content_div.find_all(string=lambda text: text and '整体界面' in text):
                    parent = element.parent
                    print(f"\n找到文本: '{element.strip()}'")
                    print(f"父元素: {parent.name}")
                    print(f"父元素class: {parent.get('class')}")
                    print(f"父元素HTML: {parent.prettify()[:300]}")
        else:
            print("未找到'整体界面'文本")
        
        # 检查面包屑导航
        print(f"\n=== 检查面包屑导航 ===")
        breadcrumbs = soup.find_all(class_=lambda x: x and 'breadcrumb' in str(x).lower())
        for breadcrumb in breadcrumbs:
            print(f"面包屑: {breadcrumb.get_text(strip=True)}")
            print(f"HTML: {breadcrumb.prettify()[:200]}")
        
        # 检查页面顶部的标题区域
        print(f"\n=== 检查页面顶部标题 ===")
        # 查找所有可能的标题容器
        for selector in ['.page-title', '.article-title', '.doc-title', '.title', 'header']:
            title_element = soup.select_one(selector)
            if title_element:
                print(f"找到标题元素 ({selector}): {title_element.get_text(strip=True)}")
                print(f"HTML: {title_element.prettify()[:200]}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_page_name())
