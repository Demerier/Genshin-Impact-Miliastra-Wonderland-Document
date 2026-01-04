# 爬虫改进记录文档

## 项目概述

本文档记录了原神千星奇域网站爬虫项目的所有改进、修复和优化，为正式爬取提供完整的技术参考。

## 改进时间线

### 第一阶段：基础功能验证（2026-01-04）

#### 1.1 链接本地化转换

**问题描述：**
- 原始爬虫将内部链接转换为完整URL
- 用户需求：将链接转换为本地相对路径，便于离线浏览

**解决方案：**
- 修改`parser.py`中的链接处理逻辑
- 识别`/ys/ugc/tutorial/`开头的内部链接
- 提取文档ID和链接文本
- 生成本地markdown文件名：`链接文本_文档ID.md`

**关键代码：**
```python
# 修复相对路径链接，转换为本地markdown文件路径
if content_div:
    for a_tag in content_div.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/ys/ugc/tutorial/'):
            if '/detail/' in href:
                doc_id = href.split('/detail/')[-1].split('?')[0]
                link_text = a_tag.get_text(strip=True)
                if link_text:
                    safe_filename = ''.join(c for c in link_text if c.isalnum() or c in (' ', '-', '_')).strip()
                    safe_filename = safe_filename.replace(' ', '_')
                    a_tag['href'] = f"{safe_filename}_{doc_id}.md"
```

**验证结果：**
- ✓ 内部链接成功转换为本地相对路径
- ✓ 文件名包含链接文本和文档ID，便于识别

#### 1.2 图片文件名优化

**问题描述：**
- 原始爬虫使用哈希值作为图片文件名，不直观
- 下载了页面其他区域的无关图片
- 用户需求：图片文件名应与文档上下文相关

**解决方案：**
1. 限制图片提取范围：仅在内容区域（`.doc-view`）查找图片
2. 改进文件名生成逻辑：包含页面名称、文档ID和上下文描述
3. 优先使用图片alt属性，其次使用周围文本

**关键代码：**
```python
# 限制图片提取范围
if content_div:
    for img_tag in content_div.find_all('img'):
        img_url = img_tag.get('data-src') or img_tag.get('src')
        if img_url:
            alt_text = img_tag.get('alt', '')
            context_text = ''
            heading = img_tag.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            if heading:
                context_text = heading.get_text(strip=True)
            if not context_text:
                next_p = img_tag.find_next('p')
                if next_p:
                    context_text = next_p.get_text(strip=True)[:30]
            local_image_path = self.download_image(img_url, context_text=context_text, alt_text=alt_text)
```

**文件名格式：**
- `页面名称_文档ID_上下文描述.png`
- 示例：`整体界面_mhn4bsi5lb58_最小化.png`

**验证结果：**
- ✓ 不再下载无关图片
- ✓ 文件名直观易懂，包含页面名称、文档ID和上下文描述
- ✓ 图片在Markdown中正确显示

#### 1.3 图片提取范围修正

**问题描述：**
- 原始爬虫在整个页面查找图片，导致下载了导航栏、页脚等区域的无关图片
- 用户反馈：图片不在文档中出现过

**解决方案：**
- 修改`parse_images`方法，限制在`content_div`（内容区域）查找图片
- 使用BeautifulSoup的`find_all`方法时指定`content_div`作为搜索范围

**关键代码：**
```python
# 替换图片URL为本地路径（仅在content_div中查找）
if content_div:
    for img_tag in content_div.find_all('img'):
        # 处理图片...
```

**验证结果：**
- ✓ 只提取内容区域的图片
- ✓ 不再下载导航栏、页脚等区域的无关图片

#### 1.4 换行问题修复

**问题描述：**
- 原网页在蓝色斜体字样前进行了换行
- Markdown转换后产生不必要的换行

**解决方案：**
- 重写`CustomMarkdownConverter`的`convert_p`方法
- 检测`<p>`标签内的多个子元素
- 手动处理所有子元素，确保它们在同一行显示

**关键代码：**
```python
def convert_p(self, el, text, parent_tags=None):
    if parent_tags is None:
        parent_tags = set()
    
    if not text or not text.strip():
        return ''
    
    # 如果<p>标签包含多个子元素，手动处理所有子元素
    if len(list(el.children)) > 1:
        result = ''
        for child in el.children:
            if hasattr(child, 'name') and child.name is not None:
                child_converter = self.get_conv_fn(child.name)
                if child_converter:
                    child_text = child_converter(child, child.get_text(), parent_tags | {el.name})
                else:
                    child_text = child.get_text()
                result += child_text
            else:
                result += str(child)
        return f'{result.strip()}\n\n'
    else:
        return f'{text}\n\n' if text else ''
```

**验证结果：**
- ✓ 蓝色斜体文本前不再有换行
- ✓ 文本在同一行正确显示

#### 1.5 页面标题保留

**问题描述：**
- Markdown文件中缺少页面标题
- 用户需求：保留每个页面的标题，如"整体界面"

**解决方案：**
- 在`trial_crawler.py`的`_save_markdown`方法中
- 在Markdown内容开头添加页面名称标题

**关键代码：**
```python
def _save_markdown(self, url: str, name: str, content: str):
    # ... 其他代码 ...
    
    # 添加页面名称标题
    markdown_content += f"## {name}\n\n"
    markdown_content += content
    
    # ... 其他代码 ...
```

**验证结果：**
- ✓ Markdown文件中包含页面名称标题
- ✓ 标题格式为二级标题（##）

#### 1.6 单独`*`符号处理

**问题描述：**
- 文档页面中存在单独的`*`符号
- 可能来源：空列表项、空段落等

**解决方案：**
- 修改`CustomMarkdownConverter`的`convert_p`方法
- 在text为空时返回空字符串
- 修改`parse_content`方法，在ul_tag中没有内容时删除所有原始列表项

**关键代码：**
```python
def convert_p(self, el, text, parent_tags=None):
    if parent_tags is None:
        parent_tags = set()
    
    # 检查text是否为空，如果为空则返回空字符串
    if not text or not text.strip():
        return ''
    
    # ... 其他代码 ...
```

**验证结果：**
- ✓ 单独`*`符号问题已解决
- ✓ 空段落和空列表项被正确处理

### 第二阶段：监控和报告系统（2026-01-04）

#### 2.1 试行爬取监控器

**功能描述：**
- 实时监控爬取进度和性能指标
- 记录页面加载时间、内容长度、图片数量等
- 生成详细的监控报告

**关键组件：**
- `CrawlMonitor`：监控器主类
- `PageMetrics`：页面指标数据类
- `TrialCrawler`：试行爬取器，集成监控功能

**监控指标：**
- 页面加载时间
- 内容长度
- 图片数量
- 链接数量
- 重试次数
- 错误次数

#### 2.2 试行爬取报告系统

**功能描述：**
- 自动分析爬取结果
- 生成详细的爬取报告
- 提供问题诊断和优化建议

**报告内容：**
- 爬取统计（成功/失败页面、总耗时等）
- 性能指标（平均加载时间、平均内容长度等）
- 资源指标（下载图片总数、提取链接总数等）
- 问题诊断和建议

#### 2.3 试行爬取配置

**配置参数：**
```python
TRIAL_CONFIG = CrawlConfig(
    request_delay_min=1.5,      # 请求延迟最小值
    request_delay_max=2.5,      # 请求延迟最大值
    max_retries=3,              # 最大重试次数
    timeout=30,                 # 超时时间
    wait_until="networkidle",   # 等待条件
    wait_timeout=30000,         # 等待超时
    additional_wait=500,        # 额外等待时间
    max_concurrent=1,           # 最大并发数
    extract_title=True,         # 提取标题
    extract_content=True,       # 提取内容
    extract_links=True,         # 提取链接
    extract_images=True,        # 提取图片
    min_content_length=100,      # 最小内容长度
    validate_links=True,         # 验证链接
    save_markdown=True,         # 保存Markdown
    save_html=False,            # 保存HTML
    markdown_dir="data/markdown_trial",  # Markdown目录
    html_dir="data/html_trial",          # HTML目录
    images_dir="data/images_trial",      # 图片目录
    log_level="DEBUG",           # 日志级别
    log_dir="logs/trial"        # 日志目录
)
```

## 技术架构

### 核心组件

1. **Parser（解析器）**
   - HTML到Markdown转换
   - 图片下载和本地化
   - 链接本地化转换
   - 自定义样式保留（红色/蓝色斜体）

2. **Downloader（下载器）**
   - Playwright浏览器自动化
   - 页面加载和等待
   - HTML内容提取

3. **TrialCrawler（试行爬取器）**
   - 爬取流程控制
   - 重试机制
   - 监控和报告

4. **CrawlMonitor（监控器）**
   - 实时监控
   - 指标收集
   - 报告生成

### 数据流

```
URL → Downloader → HTML → Parser → Markdown + Images
                              ↓
                         Links → Local Markdown Files
```

### 文件结构

```
markdown/
├── src/
│   └── crawler/
│       ├── parser.py          # 解析器
│       ├── downloader.py      # 下载器
│       └── spider.py          # 爬虫
├── data/
│   ├── markdown_trial/        # 试行Markdown文件
│   ├── html_trial/            # 试行HTML文件
│   └── images_trial/          # 试行图片文件
├── logs/
│   └── trial/                 # 试行日志
├── trial_crawler.py           # 试行爬取器
├── trial_crawl_config.py      # 试行配置
├── trial_crawl_monitor.py     # 试行监控器
├── trial_crawl_report.py      # 试行报告
└── run_trial_crawl.py          # 试行爬取入口
```

## 已知问题和限制

### 已解决问题
1. ✓ 链接本地化转换
2. ✓ 图片文件名优化
3. ✓ 图片提取范围修正
4. ✓ 换行问题修复
5. ✓ 页面标题保留
6. ✓ 单独`*`符号处理

### 当前限制
1. 单线程爬取，速度较慢
2. 无增量更新机制
3. 无断点续传功能
4. 无分布式爬取支持

### 待优化项
1. 支持多线程并发爬取
2. 实现增量更新机制
3. 添加断点续传功能
4. 优化内存使用
5. 添加更多错误处理

## 正式爬取准备

### 配置文件
- `crawl_config.py`：正式爬取配置
- `crawl_pages.py`：爬取页面列表

### 启动脚本
- `run_crawl.py`：正式爬取入口

### 监控和报告
- `crawl_monitor.py`：正式监控器
- `crawl_report.py`：正式报告生成器

## 总结

通过多个阶段的改进和优化，爬虫已经具备了以下能力：

1. **完整的本地化支持**：链接和图片都转换为本地路径
2. **直观的文件命名**：文件名包含页面名称、文档ID和上下文描述
3. **准确的提取范围**：只在内容区域提取图片和链接
4. **完善的样式保留**：保留红色/蓝色斜体等自定义样式
5. **强大的监控能力**：实时监控爬取进度和性能指标
6. **详细的报告系统**：自动生成爬取报告和优化建议

爬虫已准备好进行正式爬取。
