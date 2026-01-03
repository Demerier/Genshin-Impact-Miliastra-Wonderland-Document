"""
页面内容解析器
"""

from bs4 import BeautifulSoup
import markdownify


class Parser:
    """页面内容解析器"""
    
    def parse_content(self, soup):
        """解析页面内容
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            解析后的内容
        """
        # 尝试多种选择器定位内容区域
        content_div = soup.select_one('.doc-view')
        if not content_div:
            content_div = soup.select_one('.content')
        if not content_div:
            content_div = soup.select_one('main')
        if not content_div:
            content_div = soup.select_one('body')
        
        # 提取标题
        title = soup.title.string if soup.title else ''
        
        # 提取正文内容
        content = str(content_div)
        
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
