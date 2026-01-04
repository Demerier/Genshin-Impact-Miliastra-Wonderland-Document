#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查HTML中所有可能被转换为*的元素
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def check_asterisk_elements():
    """检查HTML中所有可能被转换为*的元素"""
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
            print("=== 查找所有可能被转换为*的元素 ===")
            
            # 查找所有ul和ol标签
            ul_tags = content_div.find_all('ul')
            ol_tags = content_div.find_all('ol')
            
            print(f"找到 {len(ul_tags)} 个ul标签")
            print(f"找到 {len(ol_tags)} 个ol标签")
            
            # 查找所有li标签
            li_tags = content_div.find_all('li')
            print(f"找到 {len(li_tags)} 个li标签")
            
            # 查找所有em和i标签（斜体）
            em_tags = content_div.find_all('em')
            i_tags = content_div.find_all('i')
            
            print(f"找到 {len(em_tags)} 个em标签")
            print(f"找到 {len(i_tags)} 个i标签")
            
            # 检查每个em和i标签
            print("\n=== 检查em和i标签 ===")
            for i, tag in enumerate(em_tags + i_tags):
                text = tag.get_text(strip=True)
                print(f"{i+1}. {tag.name}标签: '{text}'")
                if not text:
                    print(f"   警告: 空的{tag.name}标签!")
                    print(f"   HTML: {tag.prettify()[:200]}")
            
            # 查找所有span标签
            span_tags = content_div.find_all('span')
            print(f"\n找到 {len(span_tags)} 个span标签")
            
            # 检查每个span标签
            print("\n=== 检查span标签 ===")
            for i, tag in enumerate(span_tags):
                text = tag.get_text(strip=True)
                style = tag.get('style', '')
                if 'italic' in style.lower():
                    print(f"{i+1}. span标签（斜体）: '{text}'")
                    if not text:
                        print(f"   警告: 空的斜体span标签!")
                        print(f"   HTML: {tag.prettify()[:200]}")
            
            # 查找所有包含*的文本节点
            print("\n=== 查找所有包含*的文本节点 ===")
            for element in content_div.find_all(True):
                for child in element.children:
                    if hasattr(child, 'name') and child.name is None:
                        text = str(child)
                        if '*' in text:
                            print(f"找到包含*的文本节点:")
                            print(f"  父元素: {element.name}, class: {element.get('class')}")
                            print(f"  文本: '{text}'")
                            print(f"  父元素HTML: {element.prettify()[:300]}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_asterisk_elements())
