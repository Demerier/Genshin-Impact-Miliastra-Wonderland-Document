# Website Crawler Package

__version__ = "1.0.0"

# 导出主要功能
from .main import main

# 导出爬虫模块
from .crawler.spider import Spider
from .crawler.parser import Parser
from .crawler.downloader import Downloader