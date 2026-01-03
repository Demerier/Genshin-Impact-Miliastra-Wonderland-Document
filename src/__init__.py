#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
原神千星奇域·综合指南 - 网站爬取项目包

提供完整的网页爬取、解析和转换功能，用于将原神千星奇域官方文档转换为Markdown格式。
"""

__version__ = "1.0.0"

# 导出主要功能
from .main import main

# 导出爬虫模块
from .crawler.spider import Spider
from .crawler.parser import Parser
from .crawler.downloader import Downloader
