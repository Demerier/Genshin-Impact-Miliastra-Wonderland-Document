#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查页面中的所有列表元素和Markdown转换结果
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from src.crawler.parser import Parser


async def check_all_lists():
    """检查页面中的所有列表元素"""
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
            
            print("\n=== 检查Markdown转换结果 ===")
            
            # 使用Parser转换HTML为Markdown
            parser = Parser()
            result = parser.parse_content(soup)
            
            print(f"返回结果类型: {type(result)}")
            print(f"返回结果: {result}")
            
            # 查找Markdown中的*符号
            if isinstance(result, dict) and 'content' in result:
                content = result['content']
                print(f"Markdown内容长度: {len(content)}")
                print(f"Markdown内容:\n{content[:2000]}")
                
                print("\n=== 查找Markdown中的*符号 ===")
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if line.strip() == '*':
                        print(f"第{i}行: '{line}'")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_all_lists())
