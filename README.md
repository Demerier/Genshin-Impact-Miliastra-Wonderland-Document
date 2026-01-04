# 文档爬取系统

## 项目介绍

本项目是一个基于Playwright的网页爬虫系统，用于自动爬取官方文档并转换为Markdown格式，支持图片本地化和断点续爬。

## 目录结构

```
.
├── src/                 # 源代码目录
│   ├── crawler/         # 爬虫核心模块
│   │   ├── __init__.py  # 包初始化文件
│   │   ├── crawler.py   # 网页爬取器
│   │   ├── crawl_config.py # 爬虫配置
│   │   ├── downloader.py # 下载器
│   │   ├── parser.py    # 内容解析器
│   │   └── spider.py    # 爬虫主程序
│   └── examples/        # 示例代码
│       └── playwright_load_detection.py # Playwright加载检测示例
├── config/              # 配置文件目录
│   ├── __init__.py      # 包初始化文件
│   └── logging_config.py # 日志配置
├── data/                # 数据存储目录
│   ├── markdown/        # 爬取的Markdown文档
│   └── images/          # 下载的图片资源
├── archive/             # 归档目录（制作过程中产生的文件）
├── docs/                # 项目文档目录
├── logs/                # 日志文件目录
├── .gitignore           # Git忽略文件
└── README.md            # 项目说明文档
```

## 功能特性

- ✅ 自动爬取所有文档页面
- ✅ 将HTML转换为Markdown格式
- ✅ 本地化所有链接和图片资源
- ✅ 支持断点续爬
- ✅ 支持极长内容分段处理
- ✅ 完善的日志记录系统
- ✅ 质量控制机制
- ✅ 支持异步并行爬取

## 安装依赖

### 环境要求

- Python 3.8+
- pip 20.0+

### 安装步骤

1. 克隆项目仓库
2. 安装依赖包

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
python src/crawler/crawler.py
```

### 配置说明

爬虫配置位于`src/crawler/crawl_config.py`，主要配置项包括：

- `CRAWL_CONFIG`：爬虫基本配置（请求延迟、重试次数等）
- `CRAWL_PAGES`：待爬取页面列表
- `PARSING_RULES`：页面解析规则
- `EXTRACTION_FIELDS`：需要提取的字段

## 技术栈

- **Playwright**：浏览器自动化工具，用于获取动态页面内容
- **BeautifulSoup4**：HTML解析库，用于提取页面内容
- **Markdown**：Markdown转换库，用于HTML到Markdown的转换
- **Logging**：日志记录，用于系统监控和调试

## 开发流程

### 代码规范

- 遵循PEP 8规范
- 使用4空格缩进
- 变量/函数使用snake_case命名
- 类使用PascalCase命名
- 行宽≤120字符

### 提交规范

- 提交信息清晰明了
- 遵循"类型: 描述"的格式
- 类型包括：feat, fix, docs, style, refactor, test, chore

## 项目状态

- ✅ 爬虫核心功能实现（基于Playwright）
- ✅ HTML转Markdown功能
- ✅ 图片资源本地化（自动下载和存储）
- ✅ 链接本地化
- ✅ 日志系统（详细的操作日志）

## 后续计划

1. 优化页面解析算法
2. 完善质量控制机制
3. 添加单元测试
4. 实现持续集成/持续部署
5. 开发Web管理界面

## 许可证

MIT License