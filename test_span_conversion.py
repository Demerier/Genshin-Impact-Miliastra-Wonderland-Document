#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试span标签转换，特别是红色斜体和蓝色斜体文本的保留
"""

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

# 创建自定义MarkdownConverter，保留红色斜体和蓝色斜体文本
class CustomMarkdownConverter(MarkdownConverter):
    def get_conv_fn(self, tag_name):
        """
        重写get_conv_fn方法，确保span标签使用我们的自定义转换函数
        """
        if tag_name == 'span':
            return self.convert_span
        return super().get_conv_fn(tag_name)
    
    def convert_span(self, el, text, parent_tags=None):
        """
        自定义span标签转换函数，保留红色和蓝色斜体文本
        """
        if parent_tags is None:
            parent_tags = set()
        
        # 检查是否为红色或蓝色斜体文本
        style = el.get('style', '')
        class_ = el.get('class', '')
        
        # 检查是否包含颜色样式和斜体样式
        is_red = 'color: red' in style.lower() or 'color: #ff0000' in style.lower()
        is_blue = 'color: blue' in style.lower() or 'color: #0000ff' in style.lower() or 'color: #00f' in style.lower()
        is_italic = 'font-style: italic' in style.lower()
        
        # 检查是否有颜色相关的class
        if isinstance(class_, list):
            class_ = ' '.join(class_)
        
        if not is_red:
            is_red = 'red' in class_.lower() or 'c-red' in class_.lower()
        if not is_blue:
            is_blue = 'blue' in class_.lower() or 'c-blue' in class_.lower()
        if not is_italic:
            is_italic = 'italic' in class_.lower() or 'i-' in class_.lower()
        
        # 检查父标签是否包含em或i，这也表示斜体
        if not is_italic:
            if 'em' in parent_tags or 'i' in parent_tags:
                is_italic = True
        
        # 如果是红色斜体，使用HTML span保留样式
        if is_red and is_italic:
            return f'<span style="color: red; font-style: italic;">{text}</span>'
        # 如果是蓝色斜体，使用HTML span保留样式
        elif is_blue and is_italic:
            return f'<span style="color: blue; font-style: italic;">{text}</span>'
        # 如果只是红色，保留红色
        elif is_red:
            return f'<span style="color: red;">{text}</span>'
        # 如果只是蓝色，保留蓝色
        elif is_blue:
            return f'<span style="color: blue;">{text}</span>'
        # 如果只是斜体，使用Markdown斜体
        elif is_italic:
            return f'*{text}*'
        # 其他情况，直接返回文本
        return text

# 测试HTML
html_test_cases = [
    '<span style="color: red; font-style: italic;">红色斜体</span>',
    '<span style="color: blue; font-style: italic;">蓝色斜体</span>',
    '<em style="color: red;">红色斜体em</em>',
    '<i style="color: blue;">蓝色斜体i</i>',
    '<span class="red italic">红色斜体class</span>',
    '<span class="blue italic">蓝色斜体class</span>',
    '<div><span style="color: red; font-style: italic;">红色斜体在div中</span></div>',
    '<p>普通文本<span style="color: red; font-style: italic;">红色斜体</span>普通文本</p>'
]

# 测试转换
print("测试自定义span标签转换：")
print("=" * 50)

for html in html_test_cases:
    print(f"\nHTML: {html}")
    # 使用默认转换器
    default_result = MarkdownConverter().convert(html)
    print(f"默认转换: {default_result}")
    # 使用自定义转换器
    custom_result = CustomMarkdownConverter().convert(html)
    print(f"自定义转换: {custom_result}")

print("\n" + "=" * 50)
print("测试完成")
