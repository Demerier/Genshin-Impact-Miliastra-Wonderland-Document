# 应用配置文件

APP_NAME = "千星奇域提示词工程系统"
APP_VERSION = "0.1.0"

# 数据库配置
DATABASE_URL = "sqlite:///./data/qianxing.db"

# 向量数据库配置
CHROMA_DB_PATH = "./data/chroma_db"

# AI服务配置
AI_SERVICES = {
    "openai": {
        "api_key": "your-openai-api-key",
        "model": "gpt-4",
        "base_url": None,
        "timeout": 30
    },
    "wenxin": {
        "api_key": "your-wenxin-api-key",
        "secret_key": "your-wenxin-secret-key",
        "model": "ernie-bot-4",
        "timeout": 30
    },
    "tongyi": {
        "api_key": "your-tongyi-api-key",
        "model": "qwen-plus",
        "timeout": 30
    }
}

# 默认AI服务
DEFAULT_AI_SERVICE = "openai"

# 提示词配置
PROMPT_CONFIG = {
    "max_knowledge_chunks": 5,
    "max_prompt_length": 4000,
    "default_role": "game_designer",
    "default_phase": "design_planning"
}

# 日志配置
LOG_LEVEL = "INFO"
LOG_FILE = "./logs/app.log"

# API配置
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi.json"
}