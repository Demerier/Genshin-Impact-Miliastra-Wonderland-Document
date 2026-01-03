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
        
        # 预处理自定义列表结构
        if content_div:
            # 查找所有自定义列表元素
            custom_lists = content_div.find_all('div', class_='prosemirror-list-new')
            
            # 用于跟踪已处理的列表项，避免重复处理
            processed_items = set()
            
            for custom_list in custom_lists:
                # 跳过已处理的列表项或无效的列表项
                if not custom_list or custom_list in processed_items:
                    continue
                
                # 创建新的ul标签
                ul_tag = soup.new_tag('ul')
                
                # 查找所有连续的列表项（同一级别的prosemirror-list-new）
                list_items = []
                current = custom_list
                
                while True:
                    # 多重安全检查
                    if current is None:
                        break
                    
                    # 确保current是Tag类型
                    if not hasattr(current, 'get'):
                        break
                    
                    if not hasattr(current, 'find_next_sibling'):
                        break
                    
                    # 检查current是否有class属性且包含prosemirror-list-new
                    try:
                        current_class = current.get('class', [])
                        if not isinstance(current_class, list) or 'prosemirror-list-new' not in current_class:
                            break
                    except AttributeError:
                        break
                    
                    list_items.append(current)
                    processed_items.add(current)
                    
                    # 获取下一个兄弟元素
                    next_sibling = current.find_next_sibling()
                    if not next_sibling:
                        break
                    current = next_sibling
                
                # 将每个列表项转换为li标签
                for item in list_items:
                    # 获取列表内容
                    list_content = item.find('div', class_='list-content')
                    if list_content:
                        # 创建li标签
                        li_tag = soup.new_tag('li')
                        # 将列表内容添加到li标签中
                        li_tag.append(list_content)
                        # 将li标签添加到ul标签中
                        ul_tag.append(li_tag)
                
                # 替换自定义列表为标准ul列表
                if len(ul_tag.contents) > 0 and list_items:
                    # 替换第一个列表项
                    list_items[0].replace_with(ul_tag)
                    # 删除后续的列表项
                    for item in list_items[1:]:
                        if item.parent:
                            item.decompose()
        
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
            # 过滤出目标域名的链接和相对链接
            if href.startswith('https://act.mihoyo.com/ys/ugc/tutorial/detail/') or \
               href.startswith('/ys/ugc/tutorial/detail/') or \
               href.startswith('/ys/ugc/tutorial//detail/'):
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
        for img_tag in soup.find_all('img'):
            # 优先提取data-src属性，支持懒加载图片
            img_url = img_tag.get('data-src') or img_tag.get('src')
            if img_url:
                images.append(img_url)
        return images
