#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
页面内容解析器
负责将HTML页面转换为Markdown格式，并提取页面中的链接和图片。
"""

# 标准库导入
import sys
import os
import hashlib
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 第三方库导入
from bs4 import BeautifulSoup
import markdownify
from markdownify import MarkdownConverter
import requests

# 配置和日志导入
from config import logger


class Parser:
    """页面内容解析器"""

    def __init__(self, images_dir="data/images"):
        """初始化解析器

        Args:
            images_dir: 图片存储目录
        """
        self.images_dir = Path(images_dir)
        self.page_name = None
        self.doc_id = None
        # 确保图片目录存在
        self.images_dir.mkdir(parents=True, exist_ok=True)
        # 用于跟踪同一上下文下的图片数量
        self.context_image_count = {}

    def get_image_hash(self, image_url):
        """获取图片URL的哈希值，用于生成唯一文件名

        Args:
            image_url: 图片URL

        Returns:
            图片哈希值
        """
        hasher = hashlib.md5()
        hasher.update(image_url.encode('utf-8'))
        return hasher.hexdigest()

    def download_image(self, image_url, context_text=None, alt_text=None):
        """下载图片到本地

        Args:
            image_url: 图片URL
            context_text: 图片周围的上下文文本，用于生成有意义的文件名
            alt_text: 图片的alt属性文本

        Returns:
            本地图片路径
        """
        try:
            logger.info(f"开始下载图片: {image_url}")
            
            # 生成有意义的文件名
            # 格式: 页面名称_文档ID_上下文描述_序号.png
            # 例如: 整体界面_mhn4bsi5lb58_最小化_1.png
            filename_parts = []
            
            # 添加页面名称
            if self.page_name:
                safe_page_name = ''.join(c for c in self.page_name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_page_name = safe_page_name.replace(' ', '_')
                if safe_page_name:
                    filename_parts.append(safe_page_name)
            
            # 添加文档ID
            if self.doc_id:
                filename_parts.append(self.doc_id)
            
            # 添加上下文描述（优先使用alt文本，然后使用上下文文本）
            description = ''
            if alt_text:
                description = alt_text
            elif context_text:
                description = context_text[:30]
            
            # 生成上下文键，用于跟踪同一上下文下的图片数量
            context_key = '_'.join(filename_parts)
            if description:
                safe_description = ''.join(c for c in description if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_description = safe_description.replace(' ', '_')
                if safe_description:
                    filename_parts.append(safe_description)
                    context_key = '_'.join(filename_parts)
            
            # 如果没有生成任何描述部分，使用哈希值
            if not filename_parts:
                local_filename = f"{self.get_image_hash(image_url)}.png"
            else:
                # 获取当前上下文的图片序号
                if context_key not in self.context_image_count:
                    self.context_image_count[context_key] = 0
                self.context_image_count[context_key] += 1
                
                # 如果是同一上下文下的第一张图片，不添加序号
                # 否则添加序号
                if self.context_image_count[context_key] > 1:
                    filename_parts.append(str(self.context_image_count[context_key]))
                
                # 组合文件名
                local_filename = '_'.join(filename_parts) + '.png'
            
            local_path = self.images_dir / local_filename
            
            # 如果图片已存在，直接返回本地路径
            if local_path.exists():
                logger.info(f"图片已存在: {local_path}")
                return str(local_path)
            
            # 下载图片
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 保存图片
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"成功下载图片: {image_url} -> {local_path}")
            return str(local_path)
        except Exception as e:
            logger.error(f"下载图片失败 {image_url}: {e}", exc_info=True)
            return None

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
                        iframe_soup = BeautifulSoup(
                            response.text, 'html.parser')

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
            custom_lists = content_div.find_all(
                'div', class_='prosemirror-list-new')

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
                        # 检查内容是否为空
                        content_text = list_content.get_text(strip=True)
                        if content_text:  # 只添加非空内容
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
                elif list_items:
                    # 如果ul_tag中没有内容，删除所有原始列表项
                    for item in list_items:
                        if item.parent:
                            item.decompose()

        # 替换图片URL为本地路径
        if content_div:
            for img_tag in content_div.find_all('img'):
                # 优先提取data-src属性，支持懒加载图片
                img_url = img_tag.get('data-src') or img_tag.get('src')
                if img_url:
                    # 获取图片的alt文本
                    alt_text = img_tag.get('alt', '')
                    
                    # 获取图片周围的上下文文本
                    context_text = ''
                    
                    # 查找最近的标题（h1-h6）
                    heading = img_tag.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if heading:
                        context_text = heading.get_text(strip=True)
                    
                    # 如果没有找到标题，查找下一个段落
                    if not context_text:
                        next_p = img_tag.find_next('p')
                        if next_p:
                            context_text = next_p.get_text(strip=True)[:30]
                    
                    # 下载图片到本地
                    local_image_path = self.download_image(img_url, context_text=context_text, alt_text=alt_text)
                    if local_image_path:
                        # 更新img标签的src属性为相对路径
                        # 将data/images/或data/images_trial/转换为../images/，因为markdown文件位于data/markdown/或data/markdown_trial/目录下
                        relative_path = local_image_path.replace('data\\images\\', '../images/').replace('data/images/', '../images/')
                        relative_path = relative_path.replace('data\\images_trial\\', '../images/').replace('data/images_trial/', '../images/')
                        img_tag['src'] = relative_path

        # 修复相对路径链接，转换为本地markdown文件路径
        if content_div:
            for a_tag in content_div.find_all('a', href=True):
                href = a_tag['href']
                # 处理相对路径链接
                if href.startswith('/ys/ugc/tutorial/'):
                    # 移除多余的双斜杠
                    href = href.replace('//', '/')
                    # 提取文档ID
                    if '/detail/' in href:
                        doc_id = href.split('/detail/')[-1].split('?')[0]
                        # 获取链接文本作为文件名
                        link_text = a_tag.get_text(strip=True)
                        if link_text:
                            # 转换为本地markdown文件路径
                            # 文件名格式: 链接文本_文档ID.md
                            # 需要清理文件名中的特殊字符
                            safe_filename = ''.join(c for c in link_text if c.isalnum() or c in (' ', '-', '_')).strip()
                            safe_filename = safe_filename.replace(' ', '_')
                            a_tag['href'] = f"{safe_filename}_{doc_id}.md"
                        else:
                            # 如果没有链接文本，使用文档ID
                            a_tag['href'] = f"document_{doc_id}.md"
                elif href.startswith('/'):
                    # 其他相对路径保持不变或转换为绝对URL
                    from urllib.parse import urljoin
                    a_tag['href'] = urljoin('https://act.mihoyo.com', href)

        # 提取正文内容
        if content_div:
            content = str(content_div)
        else:
            content = str(soup)

        # 创建自定义MarkdownConverter，保留红色斜体和蓝色斜体文本
        class CustomMarkdownConverter(MarkdownConverter):
            def get_conv_fn(self, tag_name):
                """
                重写get_conv_fn方法，确保所有文本标签使用我们的自定义转换函数
                """
                if tag_name == 'p':
                    return self.convert_p
                elif tag_name in ['span', 'em', 'i', 'b', 'strong', 'div', 'font']:
                    return self.convert_tag
                return super().get_conv_fn(tag_name)
            
            def convert_p(self, el, text, parent_tags=None):
                """
                重写convert_p方法，避免在<p>标签内多个子元素时产生不必要的换行
                """
                if parent_tags is None:
                    parent_tags = set()
                
                # 检查text是否为空，如果为空则返回空字符串
                if not text or not text.strip():
                    return ''
                
                # 如果<p>标签包含多个子元素，我们需要特殊处理
                # 避免在每个子元素之间产生换行
                if len(list(el.children)) > 1:
                    # 手动处理所有子元素，确保它们在同一行
                    result = ''
                    for child in el.children:
                        if hasattr(child, 'name') and child.name is not None:
                            # 递归处理子标签
                            child_converter = self.get_conv_fn(child.name)
                            if child_converter:
                                child_text = child_converter(child, child.get_text(), parent_tags | {el.name})
                            else:
                                child_text = child.get_text()
                            result += child_text
                        else:
                            # 文本节点直接添加
                            result += str(child)
                    return f'{result.strip()}\n\n'
                else:
                    # 单个子元素，使用默认处理
                    return f'{text}\n\n' if text else ''
            
            def convert_tag(self, el, text, parent_tags=None):
                """
                自定义标签转换函数，保留红色和蓝色斜体文本
                处理span, em, i, b, strong, p, div等标签
                """
                if parent_tags is None:
                    parent_tags = set()
                
                tag_name = el.name
                style = el.get('style', '')
                class_ = el.get('class', '')
                color_attr = el.get('color', '')
                
                # 检查是否为红色或蓝色斜体文本
                # 扩展颜色检测，支持更多颜色值和class名称
                is_red = False
                is_blue = False
                is_italic = False
                is_bold = False
                
                # 检查style属性中的颜色
                style_lower = style.lower()
                is_red = any(color in style_lower for color in [
                    'color: red', 'color: #ff0000', 'color: #f00', 
                    'color: rgb(255, 0, 0)', 'color: rgb(255,0,0)',
                    'color:rgba(255, 0, 0', 'color:rgba(255,0,0',
                    'color: rgba(251,44,54,1)', 'color:rgba(251,44,54,1)',
                    'color: rgba(251,44,54)', 'color:rgba(251,44,54)'
                ])
                is_blue = any(color in style_lower for color in [
                    'color: blue', 'color: #0000ff', 'color: #00f', 
                    'color: #0099ff', 'color: #00aaff', 'color: #0066cc',
                    'color: rgb(0, 0, 255)', 'color: rgb(0,0,255)',
                    'color:rgba(0, 0, 255', 'color:rgba(0,0,255',
                    'color: rgba(89,111,254,1)', 'color:rgba(89,111,254,1)',
                    'color: rgba(89,111,254)', 'color:rgba(89,111,254)'
                ])
                is_italic = 'font-style: italic' in style_lower
                is_bold = any(style_str in style_lower for style_str in [
                    'font-weight: bold', 'font-weight: 700', 'font-weight: 600',
                    'font-weight:800', 'font-weight:900'
                ])
                
                # 检查color属性（旧式HTML属性）
                if color_attr:
                    color_lower = color_attr.lower()
                    if color_lower in ['red', '#ff0000', '#f00']:
                        is_red = True
                    elif color_lower in ['blue', '#0000ff', '#00f', '#0099ff', '#00aaff']:
                        is_blue = True
                
                # 检查是否有颜色相关的class
                if isinstance(class_, list):
                    class_ = ' '.join(class_)
                class_lower = class_.lower()
                
                # 扩展class检测，支持更多class名称
                if not is_red:
                    is_red = any(cls in class_lower for cls in [
                        'red', 'c-red', 'text-red', 'color-red', 'red-text', 
                        'danger', 'warning', 'text-danger', 'text-warning'
                    ])
                if not is_blue:
                    is_blue = any(cls in class_lower for cls in [
                        'blue', 'c-blue', 'text-blue', 'color-blue', 'blue-text', 
                        'info', 'primary', 'text-info', 'text-primary'
                    ])
                if not is_italic:
                    is_italic = any(cls in class_lower for cls in [
                        'italic', 'i-', 'text-italic', 'font-italic'
                    ])
                if not is_bold:
                    is_bold = any(cls in class_lower for cls in [
                        'bold', 'b-', 'text-bold', 'font-bold', 'strong'
                    ])
                
                # 检查父标签是否包含em或i，这也表示斜体
                if not is_italic:
                    if any(tag in parent_tags for tag in ['em', 'i', 'italic']):
                        is_italic = True
                
                # 检查是否有em或i子标签，这也表示斜体
                if not is_italic:
                    if el.find(['em', 'i']) is not None:
                        is_italic = True
                
                # 检查当前标签是否为em或i，这也表示斜体
                if tag_name in ['em', 'i']:
                    is_italic = True
                
                # 检查当前标签是否为b或strong，这也表示粗体
                if tag_name in ['b', 'strong']:
                    is_bold = True
                
                # 处理各种组合情况，使用HTML标签保留颜色样式
                # 如果有颜色，使用HTML标签包裹文本（移除text中已有的Markdown格式）
                if is_red or is_blue:
                    # 移除text中已有的Markdown格式（*和**）
                    clean_text = text.replace('*', '').replace('_', '')
                    if is_red and is_italic:
                        # 红色斜体 - 使用HTML标签
                        return f'<span style="color: red; font-style: italic;">{clean_text}</span>'
                    elif is_blue and is_italic:
                        # 蓝色斜体 - 使用HTML标签
                        return f'<span style="color: blue; font-style: italic;">{clean_text}</span>'
                    elif is_red and is_bold:
                        # 红色粗体 - 使用HTML标签
                        return f'<span style="color: red; font-weight: bold;">{clean_text}</span>'
                    elif is_blue and is_bold:
                        # 蓝色粗体 - 使用HTML标签
                        return f'<span style="color: blue; font-weight: bold;">{clean_text}</span>'
                    elif is_red:
                        # 红色文本 - 使用HTML标签
                        return f'<span style="color: red;">{clean_text}</span>'
                    elif is_blue:
                        # 蓝色文本 - 使用HTML标签
                        return f'<span style="color: blue;">{clean_text}</span>'
                elif is_italic:
                    # 仅斜体
                    return f'*{text}*'
                elif is_bold:
                    # 仅粗体
                    return f'**{text}**'
                else:
                    # 其他情况，根据标签类型使用默认转换
                    if tag_name == 'span':
                        return text
                    elif tag_name in ['em', 'i']:
                        return f'*{text}*'
                    elif tag_name in ['b', 'strong']:
                        return f'**{text}**'
                    elif tag_name in ['p', 'div']:
                        return f'{text}\n\n' if text else ''
                    elif tag_name == 'font':
                        # 处理旧式font标签
                        return text
                    # 其他标签使用默认转换
                    return super().convert_tag(el, text, parent_tags) if hasattr(super(), 'convert_tag') else text
        
        # 转换为Markdown格式，使用自定义转换器
        markdown_content = CustomMarkdownConverter(heading_style="ATX").convert(content)

        # 过滤掉单独的*符号行
        lines = markdown_content.split('\n')
        filtered_lines = [line for line in lines if line.strip() != '*']
        markdown_content = '\n'.join(filtered_lines)

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
            
            # 规范化URL，移除多余的斜杠
            href = href.replace('//', '/')
            # 修复https://中的双斜杠被错误替换的问题
            href = href.replace('https:/', 'https://')
            
            # 首先检查是否为目标域名的detail链接
            if href.startswith('https://act.mihoyo.com/ys/ugc/tutorial/detail/') or \
               href.startswith('/ys/ugc/tutorial/detail/'):
                links.append(href)
            # 对于测试用例和其他通用情况，接受所有同域名的链接
            else:
                # 转换为绝对URL
                from urllib.parse import urljoin, urlparse
                absolute_url = urljoin(base_url, href)
                # 检查是否为同一域名下的链接
                if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
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
        # 只在内容区域查找图片
        content_div = soup.find('div', class_='doc-view')
        if content_div:
            for img_tag in content_div.find_all('img'):
                # 优先提取data-src属性，支持懒加载图片
                img_url = img_tag.get('data-src') or img_tag.get('src')
                if img_url:
                    images.append(img_url)
        return images
