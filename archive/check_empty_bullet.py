#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查文档页面中的空项目符号
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_empty_bullet():
    """检查文档页面中的空项目符号"""
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
            print("=== 查找空的项目符号 ===")
            
            # 查找所有ul和ol标签
            for list_tag in content_div.find_all(['ul', 'ol']):
                print(f"\n找到列表标签: {list_tag.name}")
                print(f"HTML: {list_tag.prettify()[:300]}")
                
                # 检查每个li标签
                for li in list_tag.find_all('li'):
                    text = li.get_text(strip=True)
                    print(f"  li文本: '{text}'")
                    if not text or text == '':
                        print(f"    警告: 空的li标签!")
                        print(f"    HTML: {li.prettify()}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_empty_bullet())
