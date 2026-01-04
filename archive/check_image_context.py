#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查"整体界面"页面中图片的HTML结构和上下文信息
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def check_image_context():
    """检查图片的上下文信息"""
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
        
        content_div = soup.find('div', class_='doc-view')
        
        if content_div:
            print("=== 查找所有图片 ===")
            
            # 查找所有图片
            img_tags = content_div.find_all('img')
            print(f"找到 {len(img_tags)} 个图片")
            
            for i, img_tag in enumerate(img_tags):
                print(f"\n图片 {i+1}:")
                print(f"  src: {img_tag.get('src', 'N/A')}")
                print(f"  data-src: {img_tag.get('data-src', 'N/A')}")
                print(f"  alt: {img_tag.get('alt', 'N/A')}")
                
                # 获取父元素
                parent = img_tag.parent
                if parent:
                    print(f"  父元素: {parent.name}")
                    print(f"  父元素class: {parent.get('class', 'N/A')}")
                    print(f"  父元素文本: {parent.get_text(strip=True)[:100]}")
                    
                    # 获取父元素的父元素
                    grandparent = parent.parent
                    if grandparent:
                        print(f"  祖父元素: {grandparent.name}")
                        print(f"  祖父元素class: {grandparent.get('class', 'N/A')}")
                        print(f"  祖父元素文本: {grandparent.get_text(strip=True)[:100]}")
                
                # 查找前面的兄弟元素
                prev_sibling = img_tag.find_previous_sibling()
                if prev_sibling:
                    print(f"  前一个兄弟元素: {prev_sibling.name}")
                    print(f"  前一个兄弟元素文本: {prev_sibling.get_text(strip=True)[:100]}")
                
                # 查找后面的兄弟元素
                next_sibling = img_tag.find_next_sibling()
                if next_sibling:
                    print(f"  后一个兄弟元素: {next_sibling.name}")
                    print(f"  后一个兄弟元素文本: {next_sibling.get_text(strip=True)[:100]}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_image_context())
