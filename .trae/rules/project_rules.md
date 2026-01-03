# AI开发规范

## 1. 技术栈与依赖
- Python ≥ 3.8
- Playwright ≥ 1.40（核心框架，用于浏览器自动化）
- pytest ≥ 7.0（测试框架）
- BeautifulSoup4 ≥ 4.12（HTML解析）
- requests ≥ 2.31（HTTP请求）

## 2. 测试要求
- 使用pytest框架，测试文件以test_开头
- 测试覆盖率≥80%
- 爬取功能必须包含端到端测试
- 模拟真人操作需验证页面加载完整性

## 3. 禁止使用的API
- 禁止使用Selenium（统一使用Playwright）
- 禁止使用time.sleep()固定等待（必须使用Playwright智能等待）
- 禁止硬编码URL和敏感信息
- 禁止使用同步requests处理动态页面

## 4. 代码风格
- 遵循PEP 8，4空格缩进，snake_case命名
- 函数必须有类型注解和docstring
- 行宽≤120字符
- 异常处理必须记录详细日志

## 5. 架构要求
- 模块化设计，支持增量更新
- 页面加载必须使用多维度检测（networkidle、DOM、元素可见性、图片加载）
- 图片和资源必须本地化存储
- Markdown链接必须转换为本地路径

## 6. 质量控制
- 提交前运行pytest
- 确保爬取内容完整性和准确性
- 关键操作必须记录日志到logs/目录