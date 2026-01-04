#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查解析后的HTML结构
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from src.crawler.parser import Parser


async def check_parsed_html():
    """检查解析后的HTML结构"""
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
        
        # 使用Parser处理HTML
        parser = Parser()
        result = parser.parse(html_content, url)
        
        print("=== 检查解析后的HTML ===")
        
        # 重新解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        content_div = soup.find('div', class_='doc-view')
        
        if content_div:
            # 查找所有自定义列表
            custom_lists = content_div.find_all('div', class_='list-item')
            print(f"\n找到 {len(custom_lists)} 个自定义列表项")
            
            for i, list_item in enumerate(custom_lists):
                print(f"\n列表项 {i+1}:")
                print(f"  HTML: {list_item.prettify()[:300]}")
                
                # 检查list-content
                list_content = list_item.find('div', class_='list-content')
                if list_content:
                    text = list_content.get_text(strip=True)
                    print(f"  list-content文本: '{text}'")
                    if not text:
                        print(f"  警告: 空的list-content!")
                else:
                    print(f"  警告: 没有找到list-content!")
            
            # 检查转换后的ul标签
            print("\n=== 检查转换后的ul标签 ===")
            ul_tags = content_div.find_all('ul')
            print(f"找到 {len(ul_tags)} 个ul标签")
            
            for i, ul_tag in enumerate(ul_tags):
                print(f"\nul标签 {i+1}:")
                print(f"  HTML: {ul_tag.prettify()[:500]}")
                
                # 检查每个li标签
                li_tags = ul_tag.find_all('li', recursive=False)
                print(f"  包含 {len(li_tags)} 个li标签")
                
                for j, li_tag in enumerate(li_tags):
                    text = li_tag.get_text(strip=True)
                    print(f"    li {j+1} 文本: '{text}'")
                    if not text:
                        print(f"      警告: 空的li标签!")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_parsed_html())
