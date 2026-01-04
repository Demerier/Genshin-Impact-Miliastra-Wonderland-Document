#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查HTML中所有p标签的内容
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_p_tags():
    """检查HTML中所有p标签的内容"""
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
            print("=== 查找所有p标签 ===")
            
            # 查找所有p标签
            p_tags = content_div.find_all('p')
            print(f"找到 {len(p_tags)} 个p标签")
            
            for i, p_tag in enumerate(p_tags):
                text = p_tag.get_text(strip=True)
                print(f"\np标签 {i+1}:")
                print(f"  文本: '{text}'")
                print(f"  HTML: {p_tag.prettify()[:500]}")
                
                # 检查子元素
                children = list(p_tag.children)
                print(f"  子元素数量: {len(children)}")
                
                for j, child in enumerate(children):
                    if hasattr(child, 'name') and child.name:
                        print(f"    子元素 {j+1}: {child.name}, class: {child.get('class')}")
                        if child.get('class'):
                            child_text = child.get_text(strip=True)
                            print(f"      文本: '{child_text}'")
                    else:
                        print(f"    子元素 {j+1}: 文本节点: '{str(child).strip()[:100]}'")
            
            # 查找所有div标签
            print("\n=== 查找所有div标签 ===")
            div_tags = content_div.find_all('div')
            print(f"找到 {len(div_tags)} 个div标签")
            
            # 检查是否有空的div标签
            print("\n=== 检查空的div标签 ===")
            for i, div_tag in enumerate(div_tags):
                text = div_tag.get_text(strip=True)
                if not text:
                    print(f"\n空的div标签 {i+1}:")
                    print(f"  HTML: {div_tag.prettify()[:500]}")
                    print(f"  class: {div_tag.get('class')}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_p_tags())
