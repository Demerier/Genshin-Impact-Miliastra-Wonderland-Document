import json
import os
from .logging_config import logger

# 加载配置文件
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'crawl_config.json')

# 读取配置
def load_config():
    """加载配置文件"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config file: {e}")
        return {}

# 导出配置和日志记录器
config = load_config()
