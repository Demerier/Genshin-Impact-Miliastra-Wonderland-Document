#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查"整体界面"页面中图片的上下文信息，查找标题和段落
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def check_image_context_better():
    """检查图片的上下文信息，查找标题和段落"""
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
            print("=== 查找所有图片及其上下文 ===")
            
            # 查找所有图片
            img_tags = content_div.find_all('img')
            print(f"找到 {len(img_tags)} 个图片")
            
            for i, img_tag in enumerate(img_tags):
                print(f"\n图片 {i+1}:")
                print(f"  src: {img_tag.get('src', 'N/A')}")
                print(f"  data-src: {img_tag.get('data-src', 'N/A')}")
                
                # 查找最近的h1-h6标题
                heading = img_tag.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if heading:
                    print(f"  最近的标题: {heading.name}: {heading.get_text(strip=True)}")
                
                # 查找最近的p标签
                p_tag = img_tag.find_previous('p')
                if p_tag:
                    p_text = p_tag.get_text(strip=True)
                    if p_text:
                        print(f"  最近的段落: {p_text[:100]}")
                
                # 查找下一个p标签
                next_p = img_tag.find_next('p')
                if next_p:
                    next_p_text = next_p.get_text(strip=True)
                    if next_p_text:
                        print(f"  下一个段落: {next_p_text[:100]}")
                
                # 查找父元素的父元素中的标题
                parent = img_tag.parent
                if parent:
                    grandparent = parent.parent
                    if grandparent:
                        # 在祖父元素中查找标题
                        headings = grandparent.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        if headings:
                            print(f"  祖父元素中的标题: {[h.get_text(strip=True) for h in headings]}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_image_context_better())
