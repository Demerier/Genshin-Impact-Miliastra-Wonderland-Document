#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
试行爬取配置
定义试行爬取的参数、测试页面和监控指标
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class CrawlConfig:
    """爬取配置类"""
    
    # 请求频率控制
    request_delay_min: float = 1.0
    request_delay_max: float = 2.0
    max_retries: int = 3
    timeout: int = 30
    
    # 页面加载配置
    wait_until: str = "networkidle"
    wait_timeout: int = 30000
    additional_wait: int = 500
    
    # 并发控制
    max_concurrent: int = 1
    
    # 数据提取配置
    extract_title: bool = True
    extract_content: bool = True
    extract_links: bool = True
    extract_images: bool = True
    
    # 质量控制
    min_content_length: int = 100
    validate_links: bool = True
    
    # 存储配置
    save_markdown: bool = True
    save_html: bool = False
    markdown_dir: str = "data/markdown_trial"
    html_dir: str = "data/html_trial"
    images_dir: str = "data/images_trial"
    
    # 日志配置
    log_level: str = "DEBUG"
    log_dir: str = "logs/trial"


@dataclass
class TrialPage:
    """试行测试页面配置"""
    
    url: str
    name: str
    description: str
    expected_content_type: str
    priority: int = 1
    
    # 预期指标
    expected_load_time: float = 10.0
    expected_content_length: int = 500
    
    # 提取字段
    extract_fields: List[str] = field(default_factory=lambda: ["title", "content", "links", "images"])


# 试行测试页面列表（根据目标网站结构设计）
TRIAL_PAGES = [
    TrialPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mhn4bsi5lb58",
        name="整体界面",
        description="整体界面介绍页面，包含7张图片",
        expected_content_type="text/html",
        priority=1,
        expected_load_time=10.0,
        expected_content_length=1000
    ),
    TrialPage(
        url="https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0",
        name="文档页面",
        description="文档页面，包含蓝色斜体文本",
        expected_content_type="text/html",
        priority=2,
        expected_load_time=10.0,
        expected_content_length=1000
    )
]


# 页面解析规则
PARSING_RULES = {
    "content_selectors": [
        ".doc-view",
        ".content",
        "main",
        "article",
        ".article",
        ".post",
        ".page-content",
        ".entry-content",
        ".main-content",
        "#content",
        ".container",
        ".wrapper"
    ],
    
    "title_selectors": [
        "title",
        "h1",
        ".title",
        ".page-title",
        "#title"
    ],
    
    "image_selectors": [
        "img[data-src]",
        "img[src]"
    ],
    
    "link_selectors": [
        "a[href]"
    ],
    
    "list_selectors": [
        "ul",
        "ol",
        ".prosemirror-list-new"
    ],
    
    "table_selectors": [
        "table",
        ".table"
    ]
}


# 数据提取字段定义
EXTRACTION_FIELDS = {
    "title": {
        "required": True,
        "type": "str",
        "description": "页面标题"
    },
    "content": {
        "required": True,
        "type": "str",
        "description": "页面主要内容（Markdown格式）"
    },
    "links": {
        "required": False,
        "type": "list",
        "description": "页面中的链接列表"
    },
    "images": {
        "required": False,
        "type": "list",
        "description": "页面中的图片URL列表"
    },
    "load_time": {
        "required": True,
        "type": "float",
        "description": "页面加载时间（秒）"
    },
    "status_code": {
        "required": True,
        "type": "int",
        "description": "HTTP响应状态码"
    },
    "content_length": {
        "required": True,
        "type": "int",
        "description": "提取的内容长度"
    },
    "image_count": {
        "required": False,
        "type": "int",
        "description": "提取的图片数量"
    },
    "link_count": {
        "required": False,
        "type": "int",
        "description": "提取的链接数量"
    }
}


# 监控指标定义
MONITORING_METRICS = {
    "success_rate": {
        "description": "成功爬取的页面比例",
        "formula": "successful_pages / total_pages * 100"
    },
    "average_load_time": {
        "description": "平均页面加载时间",
        "formula": "sum(load_time) / total_pages"
    },
    "average_content_length": {
        "description": "平均内容长度",
        "formula": "sum(content_length) / total_pages"
    },
    "total_images_downloaded": {
        "description": "下载的图片总数",
        "formula": "sum(image_count)"
    },
    "total_links_extracted": {
        "description": "提取的链接总数",
        "formula": "sum(link_count)"
    },
    "retry_count": {
        "description": "重试次数",
        "formula": "sum(retries)"
    },
    "error_count": {
        "description": "错误次数",
        "formula": "sum(errors)"
    }
}


# 试行爬取配置实例
TRIAL_CONFIG = CrawlConfig(
    request_delay_min=1.5,
    request_delay_max=2.5,
    max_retries=3,
    timeout=30,
    wait_until="networkidle",
    wait_timeout=30000,
    additional_wait=500,
    max_concurrent=1,
    extract_title=True,
    extract_content=True,
    extract_links=True,
    extract_images=True,
    min_content_length=100,
    validate_links=True,
    save_markdown=True,
    save_html=False,
    markdown_dir="data/markdown_trial",
    html_dir="data/html_trial",
    images_dir="data/images_trial",
    log_level="DEBUG",
    log_dir="logs/trial"
)
