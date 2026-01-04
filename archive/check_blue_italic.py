#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查蓝色斜体文本的HTML结构
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_blue_italic():
    """检查蓝色斜体文本的HTML结构"""
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
            print("=== 查找包含'蓝色斜体'的段落 ===")
            for p_tag in content_div.find_all('p'):
                text = p_tag.get_text()
                if '蓝色斜体' in text:
                    print(f"\n找到段落:")
                    print(f"  文本内容: {text}")
                    print(f"\n  HTML结构:")
                    print(f"  {p_tag.prettify()}")
                    
                    # 查找所有span标签
                    print(f"\n  查找span标签:")
                    for span in p_tag.find_all('span'):
                        style = span.get('style', '')
                        class_ = span.get('class', '')
                        print(f"    span文本: {span.get_text(strip=True)}")
                        print(f"    span style: {style}")
                        print(f"    span class: {class_}")
                    print("-" * 60)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_blue_italic())
