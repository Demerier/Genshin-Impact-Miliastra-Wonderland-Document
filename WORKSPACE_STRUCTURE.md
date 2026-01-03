# 工作区结构说明文档

## 1. 项目概述

本项目是一个用于爬取原神千星奇域·综合指南网站的Python爬虫项目，旨在将网站上的所有文档页面转换为Markdown格式便于阅读和管理。

## 2. 目录结构

```
markdown/
├── data/                # 数据存储目录
│   ├── images/          # 下载的图片资源
│   ├── markdown/        # 爬取的Markdown文档
│   ├── long_content_files.txt # 长内容文件列表
│   ├── long_content_report.md # 长内容报告
│   ├── project_summary_report.md # 项目总结报告
│   └── url_list.txt     # 爬取URL列表
├── debug/               # 调试文件目录
│   └── full_page.html   # 调试用的完整页面HTML
├── docs/                # 文档资料目录
│   ├── CODE_REVIEW_GUIDELINES.md # 代码审查指南
│   ├── COMMIT_GUIDELINES.md # 提交规范
│   ├── DOCUMENT_CHANGE_NOTIFICATION.md # 文档变更通知
│   ├── DOCUMENTATION_INDEX.md # 文档索引
│   ├── TEST_REPORT.md   # 测试报告
│   ├── VERSIONING_GUIDELINES.md # 版本控制规范
│   ├── 后续工作计划.md   # 后续工作计划
│   ├── 人工审议意见表.md   # 人工审议相关表单
│   ├── 成果物收集表.md     # 成果物收集相关表单
│   ├── 成果物自检规范.md   # 成果物自检规范
│   ├── 网站导航结构报告.md # 网站导航结构分析报告
│   ├── 网站爬取执行计划.md # 爬取执行计划
│   ├── 页面分析报告.md     # 页面分析报告
│   └── 项目进度管理计划.md # 项目进度管理计划
├── logs/                # 日志文件目录
│   ├── crawl_log.txt    # 爬虫日志
│   └── crawl_log_*.txt  # 按时间命名的爬虫日志
├── src/                 # 源代码目录
│   ├── config/          # 配置模块
│   │   └── __init__.py  # 配置初始化
│   ├── crawler/         # 爬虫核心模块
│   │   ├── __init__.py  # 爬虫模块初始化
│   │   ├── downloader.py # 下载器模块
│   │   ├── parser.py    # 解析器模块
│   │   └── spider.py    # 爬虫模块
│   ├── tests/           # 测试模块
│   │   └── test_crawler.py # 爬虫测试用例
│   ├── utils/           # 工具函数
│   │   └── __init__.py  # 工具模块初始化
│   ├── ai_full_inspection.py # AI全面自检脚本
│   ├── check_crawl_results.py # 爬取结果检查脚本
│   ├── fix_format_issues.py # 格式问题修复脚本
│   ├── identify_long_content.py # 长内容识别脚本
│   ├── initial_data_collection.py # 初始数据收集脚本
│   ├── main.py          # 主程序入口
│   └── test_crawl.py    # 爬虫测试脚本
├── tests/               # 测试目录
│   └── test_parser.py   # 解析器测试用例
├── CHANGELOG.md         # 项目变更日志
├── README.md            # 项目说明文档
├── debug_page.py        # 调试页面脚本
├── requirements.txt     # 第三方依赖列表
└── WORKSPACE_STRUCTURE.md # 工作区结构说明文档
```

## 3. 目录与文件用途说明

### 3.1 data/

用于存储爬取的数据和资源。

- `images/`：存放从网页中下载的图片资源。
- `markdown/`：存放爬取并转换后的Markdown文档。
- `long_content_files.txt`：记录所有长内容文件的列表。
- `long_content_report.md`：长内容文件的分析报告。
- `project_summary_report.md`：项目的综合总结报告。
- `url_list.txt`：爬取的URL列表。

### 3.2 debug/

存放调试相关的文件。

- `full_page.html`：用于调试的完整页面HTML文件。

### 3.3 docs/

存放项目相关的文档资料，包括计划、报告、规范等。

- `CODE_REVIEW_GUIDELINES.md`：代码审查指南
- `COMMIT_GUIDELINES.md`：提交规范
- `DOCUMENT_CHANGE_NOTIFICATION.md`：文档变更通知机制
- `DOCUMENTATION_INDEX.md`：项目文档索引
- `TEST_REPORT.md`：测试报告
- `VERSIONING_GUIDELINES.md`：版本控制规范
- `后续工作计划.md`：项目后续工作计划
- `人工审议意见表.md`：人工审议相关表单
- `成果物收集表.md`：成果物收集相关表单
- `成果物自检规范.md`：成果物自检规范
- `网站导航结构报告.md`：网站导航结构分析报告
- `网站爬取执行计划.md`：爬取执行计划
- `页面分析报告.md`：页面分析报告
- `项目进度管理计划.md`：项目进度管理计划

### 3.4 logs/

存放项目运行过程中产生的日志文件，便于调试和监控。

- `crawl_log.txt`：最新的爬虫日志文件。
- `crawl_log_*.txt`：按时间命名的历史爬虫日志文件。

### 3.5 src/

项目的源代码目录，包含所有核心功能实现。

- `config/`：配置相关的模块和工具。
  - `__init__.py`：配置模块初始化文件，包含爬虫配置、路径配置等。

- `crawler/`：爬虫核心功能模块。
  - `__init__.py`：爬虫模块初始化文件。
  - `downloader.py`：下载器模块，负责下载和保存文件。
  - `parser.py`：解析器模块，负责解析网页内容并转换为Markdown。
  - `spider.py`：爬虫模块，负责发起请求和管理爬取流程。

- `tests/`：源代码测试模块。
  - `test_crawler.py`：爬虫功能的测试用例。

- `utils/`：通用工具函数模块。
  - `__init__.py`：工具模块初始化文件。

- `ai_full_inspection.py`：AI全面自检脚本，用于检查项目成果物的质量。
- `check_crawl_results.py`：爬取结果检查脚本，用于验证爬取结果的完整性和正确性。
- `fix_format_issues.py`：格式问题修复脚本，用于自动修复Markdown格式问题。
- `identify_long_content.py`：长内容识别脚本，用于识别和处理过长的文档。
- `initial_data_collection.py`：初始数据收集脚本，用于收集网站的初始数据。
- `main.py`：项目主程序入口，负责协调各个模块的工作。
- `test_crawl.py`：简单的爬虫测试脚本，用于快速测试爬虫功能。

### 3.6 tests/

存放项目的测试文件，包括单元测试、集成测试等。

- `test_parser.py`：解析器功能的测试用例。

### 3.7 根目录文件

- `CHANGELOG.md`：项目变更日志，记录所有重要变更。
- `.gitignore`：Git忽略文件配置，指定哪些文件不被Git跟踪。
- `debug_page.py`：调试页面脚本，用于调试页面解析。
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
- 文档应保持更新，与项目实际情况一致

## 10. 开发流程

1. 从`develop`分支创建功能分支
2. 实现功能，编写测试
3. 提交代码，确保通过所有测试
4. 创建Pull Request，请求合并到`develop`分支
5. 代码审查通过后，合并到`develop`分支
6. 发布新版本时，合并`develop`分支到`main`分支并创建标签

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
- 添加自动文档更新机制，实现文档的动态维护

## 13. 联系方式

如有任何问题或建议，请联系项目负责人。

---

本文档旨在帮助AI和人类理解项目的结构和组织方式，便于后续开发和维护。请定期更新本文档，确保其与项目实际情况一致。
