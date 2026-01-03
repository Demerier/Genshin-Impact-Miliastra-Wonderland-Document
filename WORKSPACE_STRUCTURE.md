# 工作区结构说明文档

## 1. 项目概述

本项目是一个用于爬取原神千星奇域·综合指南网站的Python爬虫项目，旨在将网站上的所有文档页面转换为Markdown格式便于阅读和管理。

## 2. 目录结构

```
markdown/
├── config/              # 配置文件目录
│   ├── __init__.py      # 配置模块初始化
│   ├── crawl_config.json # 爬取配置
│   └── logging_config.py # 日志配置
├── data/                # 数据存储目录
│   ├── raw/             # 原始数据
│   │   └── url_list.txt # 爬取URL列表
│   ├── processed/       # 处理后的数据
│   │   ├── doc_id_map.json # 文档ID映射表
│   │   ├── issue_tracking.json # 问题跟踪
│   │   └── long_content_files.txt # 长内容文件列表
│   ├── markdown/        # 爬取的Markdown文档
│   └── images/          # 下载的图片资源
├── debug/               # 调试文件目录
│   ├── full_page.html   # 调试用的完整页面HTML
│   └── debug_page.py    # 调试页面脚本
├── docs/                # 文档资料目录
│   ├── guidelines/      # 规范文档
│   │   ├── CODE_REVIEW_GUIDELINES.md
│   │   ├── COMMIT_GUIDELINES.md
│   │   ├── DOCUMENT_CHANGE_NOTIFICATION.md
│   │   ├── DOCUMENTATION_INDEX.md
│   │   └── VERSIONING_GUIDELINES.md
│   ├── plans/           # 计划文档
│   │   ├── 后续工作计划.md
│   │   ├── 网站爬取执行计划.md
│   │   └── 项目进度管理计划.md
│   ├── reports/         # 报告文档
│   │   ├── ai_inspection_report.md
│   │   ├── change_history.md
│   │   ├── crawl_check_report.md
│   │   ├── crawl_report_phase1.md
│   │   ├── crawl_report_phase2.md
│   │   ├── crawl_report_phase3.md
│   │   ├── crawl_report_total.md
│   │   ├── long_content_report.md
│   │   ├── project_summary_report.md
│   │   ├── TEST_REPORT.md
│   │   ├── 网站导航结构报告.md
│   │   ├── 页面分析报告.md
│   │   └── 项目现状总结报告.md
│   └── forms/           # 表单文档
│       ├── 人工审议意见表.md
│       ├── 成果物收集表.md
│       └── 成果物自检规范.md
├── logs/                # 日志文件目录
├── scripts/             # 辅助脚本目录
│   ├── ai_full_inspection.py
│   ├── check_crawl_results.py
│   ├── fix_format_issues.py
│   ├── identify_long_content.py
│   ├── initial_data_collection.py
│   └── test_crawl.py
├── src/                 # 源代码目录
│   ├── __init__.py      # 项目包初始化
│   ├── main.py          # 主程序入口
│   ├── crawler/         # 爬虫核心模块
│   │   ├── __init__.py
│   │   ├── spider.py    # 爬虫模块
│   │   ├── parser.py    # 解析器模块
│   │   └── downloader.py # 下载器模块
│   ├── utils/           # 工具函数
│   │   └── __init__.py
│   └── services/        # 业务服务模块
│       └── __init__.py
├── tests/               # 测试目录
│   ├── __init__.py
│   ├── test_crawler.py
│   └── test_parser.py
├── .gitignore           # Git忽略文件
├── CHANGELOG.md         # 项目变更日志
├── README.md            # 项目说明文档
├── requirements.txt     # 第三方依赖列表
└── WORKSPACE_STRUCTURE.md # 工作区结构说明文档
```

## 3. 目录与文件用途说明

### 3.1 config/

用于存储项目的配置文件。

- `__init__.py`：配置模块初始化文件，加载和导出配置。
- `crawl_config.json`：爬取相关配置，如并发数、超时时间等。
- `logging_config.py`：日志配置，定义日志格式和输出位置。

### 3.2 data/

用于存储爬取的数据和资源。

- `raw/`：存放原始数据，如URL列表。
- `processed/`：存放处理后的数据，如文档ID映射表、长内容文件列表等。
- `markdown/`：存放爬取并转换后的Markdown文档。
- `images/`：存放从网页中下载的图片资源。

### 3.3 debug/

存放调试相关的文件。

- `full_page.html`：用于调试的完整页面HTML文件。
- `debug_page.py`：调试页面脚本，用于调试页面解析。

### 3.4 docs/

存放项目相关的文档资料，包括规范、计划、报告和表单等。

- `guidelines/`：规范文档，如代码审查指南、提交规范等。
- `plans/`：计划文档，如后续工作计划、爬取执行计划等。
- `reports/`：报告文档，如爬取报告、测试报告等。
- `forms/`：表单文档，如人工审议意见表、成果物收集表等。

### 3.5 logs/

存放项目运行过程中产生的日志文件，便于调试和监控。

### 3.6 scripts/

存放辅助脚本，用于执行各种辅助任务。

- `ai_full_inspection.py`：AI全面自检脚本。
- `check_crawl_results.py`：爬取结果检查脚本。
- `fix_format_issues.py`：格式问题修复脚本。
- `identify_long_content.py`：长内容识别脚本。
- `initial_data_collection.py`：初始数据收集脚本。
- `test_crawl.py`：爬虫测试脚本。

### 3.7 src/

项目的源代码目录，包含所有核心功能实现。

- `__init__.py`：项目包初始化文件，导出主要功能和版本信息。
- `main.py`：项目主程序入口，负责协调各个模块的工作。
- `crawler/`：爬虫核心功能模块。
  - `__init__.py`：爬虫模块初始化文件。
  - `spider.py`：爬虫模块，负责发起请求和管理爬取流程。
  - `parser.py`：解析器模块，负责解析网页内容并转换为Markdown。
  - `downloader.py`：下载器模块，负责下载和保存文件。
- `utils/`：通用工具函数模块。
  - `__init__.py`：工具模块初始化文件。
- `services/`：业务服务模块，处理业务逻辑。
  - `__init__.py`：服务模块初始化文件。

### 3.8 tests/

存放项目的测试文件，包括单元测试、集成测试等。

- `__init__.py`：测试模块初始化文件。
- `test_crawler.py`：爬虫功能的测试用例。
- `test_parser.py`：解析器功能的测试用例。

### 3.9 根目录文件

- `.gitignore`：Git忽略文件配置，指定哪些文件不被Git跟踪。
- `CHANGELOG.md`：项目变更日志，记录所有重要变更。
- `README.md`：项目说明文档，包含项目概述、功能特性、使用方法等。
- `requirements.txt`：第三方依赖列表，包含项目所需的所有外部库。
- `WORKSPACE_STRUCTURE.md`：工作区结构说明文档，描述项目的目录结构和文件用途。

## 4. 文件命名规范

### 4.1 源代码文件

- 使用小写字母和下划线（snake_case）命名
- 文件名应具有描述性，清晰表达文件的功能
- 模块初始化文件使用`__init__.py`

### 4.2 配置文件

- 使用小写字母和下划线（snake_case）命名
- 配置文件应使用JSON格式
- 文件名应包含配置的类型或用途

### 4.3 文档文件

- 使用英文命名时，首字母大写（PascalCase）或小写字母加下划线（snake_case）
- 使用中文命名时，直接使用中文描述
- 文档文件应使用Markdown格式（.md）

## 5. 依赖管理

项目使用`requirements.txt`文件管理第三方依赖，包含以下依赖：

- `requests`：用于发送HTTP请求
- `beautifulsoup4`：用于解析HTML内容
- `markdownify`：用于将HTML转换为Markdown
- `playwright`：处理SPA页面
- `pytest`：用于编写和运行测试

安装依赖：

```bash
pip install -r requirements.txt
```

## 6. 配置管理

- 配置文件集中存放于`config/`目录
- 支持不同环境的配置文件（如开发环境、生产环境）
- 配置参数应包含默认值，便于快速启动项目

## 7. 日志管理

- 日志文件存放于`logs/`目录
- 支持不同级别的日志输出（DEBUG、INFO、WARNING、ERROR）
- 日志格式应包含时间、级别、消息等信息

## 8. 测试管理

- 测试文件存放于`tests/`目录
- 使用`pytest`框架编写测试
- 测试文件应与源代码文件对应，便于维护

## 9. 文档管理

- 项目文档存放于`docs/`目录
- 使用Markdown格式编写文档
- 文档按类型分类存放于子目录中
- 文档应保持更新，与项目实际情况一致

## 10. 开发流程

1. 从`main`分支创建功能分支
2. 实现功能，编写测试
3. 运行所有测试，确保通过
4. 创建Pull Request，请求合并到`main`分支
5. 代码审查通过后，合并到`main`分支
6. 发布新版本时，创建标签

## 11. 最佳实践

- 保持代码简洁、可读性高
- 遵循PEP 8代码规范
- 编写详细的文档和注释
- 确保测试覆盖率
- 定期更新依赖
- 使用Git进行版本控制，遵循提交规范

## 12. 后续优化建议

- 实现断点续爬功能，支持从上次中断的地方继续爬取
- 优化长内容的分段策略，提高分段的合理性和可读性
- 增强AI自检功能，提高自动化测试覆盖率
- 实现更智能的链接处理，支持更多类型的链接转换
- 优化爬取速度和资源使用，提高并发处理能力
- 添加监控和告警功能，实时监控爬取进度和质量
- 实现更完善的错误处理和重试机制
- 支持分布式爬取功能，提高大规模爬取的效率
- 增强Markdown转换质量，支持更多HTML元素和样式

## 13. 联系方式

如有任何问题或建议，请联系项目负责人。

---

本文档旨在帮助AI和人类理解项目的结构和组织方式，便于后续开发和维护。请定期更新本文档，确保其与项目实际情况一致。