"""
页面内容解析器
"""

from bs4 import BeautifulSoup
import markdownify
import requests

# 添加日志支持
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import logger


class Parser:
    """页面内容解析器"""
    
    def parse_content(self, soup):
        """解析页面内容
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析后的内容
        """
        # 提取标题
        title = soup.title.string if soup.title else ''
        
        # 尝试多种选择器定位内容区域
        content_div = None
        
        # 1. 尝试查找所有可能的内容容器
        selectors = [
            '.doc-view', '.content', 'main', 'article', '.article', 
            '.post', '.page-content', '.entry-content', '.main-content',
            '#content', '.container', '.wrapper'
        ]
        
        for selector in selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # 检查内容长度，排除过小的容器
                if len(content_div.get_text(strip=True)) > 10:
                    break
        
        # 2. 如果没有找到合适的容器，尝试从iframe中获取
        if not content_div or len(content_div.get_text(strip=True)) <= 10:
            logger.info("尝试从iframe中获取内容")
            iframe = soup.find('iframe')
            if iframe:
                iframe_url = iframe.get('src')
                if iframe_url:
                    try:
                        # 直接获取iframe内容
                        session = requests.Session()
                        session.headers.update({
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        })
                        response = session.get(iframe_url)
                        response.raise_for_status()
                        iframe_soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # 在iframe中再次尝试查找内容
                        for selector in selectors:
                            content_div = iframe_soup.select_one(selector)
                            if content_div and len(content_div.get_text(strip=True)) > 10:
                                break
                    except Exception as e:
                        logger.error(f"Failed to get iframe content: {e}")
        
        # 3. 如果仍然没有找到，使用body
        if not content_div:
            content_div = soup.body
        
        # 提取正文内容
        if content_div:
            content = str(content_div)
        else:
            content = str(soup)
        
        # 转换为Markdown格式
        markdown_content = markdownify.markdownify(content, heading_style="ATX")
        
        return {
            'title': title,
            'content': markdown_content
        }
    
    def parse_links(self, soup, base_url):
        """解析页面中的链接
        
        Args:
            soup: BeautifulSoup对象
            base_url: 基础URL
            
        Returns:
            链接列表
        """
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # 过滤出目标域名的链接
            if href.startswith('https://act.mihoyo.com/ys/ugc/tutorial/detail/'):
                links.append(href)
        return links
    
    def parse_images(self, soup):
        """解析页面中的图片
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            图片URL列表
        """
        images = []
        for img_tag in soup.find_all('img', src=True):
            src = img_tag['src']
            images.append(src)
        return images
