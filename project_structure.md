# 项目结构

```
qianxing-prompt-engine/
├── app/                      # 主应用目录
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── knowledge/           # 知识库模块
│   │   ├── __init__.py
│   │   ├── models.py        # 数据模型
│   │   ├── repository.py    # 数据访问层
│   │   ├── service.py       # 业务逻辑层
│   │   └── parser.py        # 文档解析器
│   ├── prompt/              # 提示词模块
│   │   ├── __init__.py
│   │   ├── generator.py     # 提示词生成器
│   │   ├── templates.py     # 提示词模板
│   │   └── optimizer.py     # 提示词优化器
│   ├── ai/                  # AI服务模块
│   │   ├── __init__.py
│   │   ├── adapter.py       # AI服务适配器
│   │   ├── openai.py        # OpenAI适配器
│   │   ├── wenxin.py        # 文心一言适配器
│   │   └── tongyi.py        # 通义千问适配器
│   └── api/                 # API路由
│       ├── __init__.py
│       ├── prompts.py       # 提示词相关API
│       ├── ai.py            # AI调用相关API
│       └── knowledge.py     # 知识库相关API
├── data/                    # 数据目录
│   ├── knowledge/           # 知识库数据
│   └── prompts/             # 提示词模板
├── tests/                   # 测试目录
│   ├── test_knowledge.py
│   ├── test_prompt.py
│   └── test_ai.py
├── scripts/                 # 脚本目录
│   ├── init_db.py           # 数据库初始化脚本
│   └── import_knowledge.py  # 知识导入脚本
├── requirements.txt         # 依赖列表
├── Dockerfile               # Docker配置
└── README.md                # 项目说明
```