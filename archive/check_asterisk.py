#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查文档页面中单独*符号的来源
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_asterisk():
    """检查文档页面中的*符号"""
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
            print("=== 查找所有包含*的文本节点 ===")
            
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
            
            print("\n=== 查找所有包含*的元素 ===")
            
            # 查找所有包含*的元素
            for element in content_div.find_all(True):
                text = element.get_text(strip=True)
                if text == '*':
                    print(f"\n找到只包含*的元素:")
                    print(f"  元素: {element.name}")
                    print(f"  元素class: {element.get('class')}")
                    print(f"  元素HTML: {element.prettify()[:500]}")
                    print(f"  文本内容: '{text}'")
                    
                    # 检查父元素
                    parent = element.parent
                    if parent:
                        print(f"  父元素: {parent.name}")
                        print(f"  父元素class: {parent.get('class')}")
                        print(f"  父元素HTML: {parent.prettify()[:500]}")
            
            print("\n=== 查找所有ul和ol标签 ===")
            
            # 查找所有ul和ol标签
            for list_tag in content_div.find_all(['ul', 'ol']):
                print(f"\n找到列表标签: {list_tag.name}")
                print(f"HTML: {list_tag.prettify()[:400]}")
                
                # 检查每个li标签
                for li in list_tag.find_all('li', recursive=False):
                    text = li.get_text(strip=True)
                    print(f"  li文本: '{text}'")
                    if not text or text == '':
                        print(f"    警告: 空的li标签!")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_asterisk())
