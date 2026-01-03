# 原神千星奇域·综合指南 - 网站爬取项目

## 项目介绍

本项目旨在爬取原神千星奇域·综合指南网站的所有文档页面，转换为Markdown格式便于阅读和管理。

## 目标网站

- **网站地址**：https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0
- **内容类型**：游戏创作工具的综合指南文档
- **页面数量**：167个文档页面

## 目录结构

```
website-crawler/
├── src/                 # 源代码目录
│   ├── main.py          # 主程序入口
│   ├── crawler/         # 爬虫核心模块
│   ├── utils/           # 工具函数
│   └── config/          # 配置模块
├── config/              # 配置文件目录
├── data/                # 数据存储目录
│   ├── markdown/        # 爬取的Markdown文档
│   └── images/          # 下载的图片资源
├── logs/                # 日志文件目录
├── docs/                # 文档资料目录
├── tests/               # 测试目录
├── requirements.txt     # 第三方依赖列表
├── README.md            # 项目说明文档
└── .gitignore           # Git忽略文件
```

## 功能特性

- 自动爬取所有文档页面
- 将HTML转换为Markdown格式
- 本地化所有链接和图片资源
- 支持断点续爬
- 支持极长内容分段处理
- 完善的日志记录
- 质量控制机制

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 配置爬取参数（config/crawl_config.json）
2. 运行主程序

```bash
python src/main.py
```

## 爬取策略

- 按导航结构顺序爬取
- 采用异步并行爬取，最大并发数为5
- 每个请求间隔1-2秒
- 支持断点续爬

## 质量控制

- 自动检查内容完整性
- 验证链接有效性
- 确保格式一致性
- 支持人工审议

## 文档资料

详细的文档资料存放于`docs/`目录，包括：

- 网站爬取执行计划
- 网站导航结构报告
- 页面分析报告
- 项目进度管理计划
- 成果物自检规范
- 成果物收集表
- 人工审议意见表

## 许可证

MIT License
