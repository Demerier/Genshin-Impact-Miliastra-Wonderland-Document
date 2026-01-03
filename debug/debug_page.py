#!/usr/bin/env python3
"""
调试脚本，用于查看页面的HTML结构
"""

import requests
from bs4 import BeautifulSoup
import os

# 测试URL
TEST_URL = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"

# 保存调试信息的目录
DEBUG_DIR = "debug"
os.makedirs(DEBUG_DIR, exist_ok=True)

def main():
    """主函数"""
    print(f"调试页面: {TEST_URL}")
    
    # 发送请求获取页面内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://act.mihoyo.com/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }
    
    try:
        response = requests.get(TEST_URL, headers=headers)
        response.raise_for_status()
        
        # 保存完整HTML到文件
        with open(os.path.join(DEBUG_DIR, "full_page.html"), 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("已保存完整HTML到 debug/full_page.html")
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 定义内容选择器
        content_selectors = [
            '.doc-view', '.content', 'main', 'article', '.article',
            '.post', '.page-content', '.entry-content', '.main-content',
            '#content', '.container', '.wrapper', 'body', 'html'
        ]
        
        # 打印页面标题
        print(f"\n页面标题: {soup.title.string if soup.title else '无标题'}")
        
        # 查找所有iframe
        iframes = soup.find_all('iframe')
        print(f"\n找到 {len(iframes)} 个iframe:")
        
        for i, iframe in enumerate(iframes):
            iframe_url = iframe.get('src')
            print(f"iframe {i+1}: {iframe_url}")
            
            if iframe_url:
                try:
                    # 获取iframe内容
                    iframe_response = requests.get(iframe_url, headers=headers)
                    iframe_response.raise_for_status()
                    
                    # 保存iframe内容到文件
                    with open(os.path.join(DEBUG_DIR, f"iframe_{i+1}.html"), 'w', encoding='utf-8') as f:
                        f.write(iframe_response.text)
                    print(f"已保存iframe {i+1} 内容到 debug/iframe_{i+1}.html")
                    
                    # 解析iframe内容
                    iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                    print(f"iframe {i+1} 标题: {iframe_soup.title.string if iframe_soup.title else '无标题'}")
                    print(f"iframe {i+1} 正文长度: {len(iframe_soup.get_text())} 字符")
                    
                    print(f"\n在iframe {i+1} 中尝试查找内容容器:")
                    for selector in content_selectors:
                        content_div = iframe_soup.select_one(selector)
                        if content_div:
                            text_length = len(content_div.get_text(strip=True))
                            print(f"  {selector}: 找到，文本长度: {text_length} 字符")
                            if text_length > 10:
                                # 保存找到的内容到文件
                                with open(os.path.join(DEBUG_DIR, f"iframe_{i+1}_content.html"), 'w', encoding='utf-8') as f:
                                    f.write(str(content_div))
                                print(f"  已保存 {selector} 内容到 debug/iframe_{i+1}_content.html")
                except Exception as e:
                    print(f"  获取iframe {i+1} 内容失败: {e}")
        
        # 查找主页面中的内容容器
        print(f"\n在主页面中尝试查找内容容器:")
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                text_length = len(content_div.get_text(strip=True))
                print(f"  {selector}: 找到，文本长度: {text_length} 字符")
                if text_length > 10:
                    # 保存找到的内容到文件
                    with open(os.path.join(DEBUG_DIR, f"main_content_{selector.replace('.', '_').replace('#', '')}.html"), 'w', encoding='utf-8') as f:
                        f.write(str(content_div))
                    print(f"  已保存 {selector} 内容到 debug/main_content_{selector.replace('.', '_').replace('#', '')}.html")
        
    except Exception as e:
        print(f"获取页面失败: {e}")

if __name__ == "__main__":
    main()
