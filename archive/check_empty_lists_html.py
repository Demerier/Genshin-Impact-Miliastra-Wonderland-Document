#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查HTML中是否有空的ul或ol标签
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_empty_lists_in_html():
    """检查HTML中是否有空的ul或ol标签"""
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
            print("=== 查找所有ul和ol标签 ===")
            
            # 查找所有ul和ol标签
            ul_tags = content_div.find_all('ul')
            ol_tags = content_div.find_all('ol')
            
            print(f"找到 {len(ul_tags)} 个ul标签")
            print(f"找到 {len(ol_tags)} 个ol标签")
            
            for i, ul_tag in enumerate(ul_tags):
                print(f"\nul标签 {i+1}:")
                print(f"  HTML: {ul_tag.prettify()[:800]}")
                
                # 检查每个li标签
                li_tags = ul_tag.find_all('li', recursive=False)
                print(f"  包含 {len(li_tags)} 个li标签")
                
                for j, li_tag in enumerate(li_tags):
                    text = li_tag.get_text(strip=True)
                    print(f"    li {j+1} 文本: '{text}'")
                    if not text:
                        print(f"      警告: 空的li标签!")
                        print(f"      li HTML: {li_tag.prettify()[:200]}")
            
            for i, ol_tag in enumerate(ol_tags):
                print(f"\nol标签 {i+1}:")
                print(f"  HTML: {ol_tag.prettify()[:800]}")
                
                # 检查每个li标签
                li_tags = ol_tag.find_all('li', recursive=False)
                print(f"  包含 {len(li_tags)} 个li标签")
                
                for j, li_tag in enumerate(li_tags):
                    text = li_tag.get_text(strip=True)
                    print(f"    li {j+1} 文本: '{text}'")
                    if not text:
                        print(f"      警告: 空的li标签!")
                        print(f"      li HTML: {li_tag.prettify()[:200]}")
            
            print("\n=== 查找所有包含*的文本节点 ===")
            
            # 查找所有文本节点
            for element in content_div.find_all(True):
                # 获取所有子节点
                for child in element.children:
                    # 检查是否为NavigableString（文本节点）
                    if hasattr(child, 'name') and child.name is None:
                        text = str(child).strip()
                        if text == '*':
                            print(f"\n找到单独的*符号:")
                            print(f"  父元素: {element.name}")
                            print(f"  父元素class: {element.get('class')}")
                            print(f"  父元素HTML: {element.prettify()[:500]}")
                            print(f"  文本内容: '{text}'")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_empty_lists_in_html())
