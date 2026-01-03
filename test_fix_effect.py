#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复效果的脚本
验证所有修复项是否生效
"""

import os
import re
import json
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) if __name__ == "__main__" else sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 测试数据目录
TEST_MARKDOWN_DIR = "data/test_markdown"
TEST_IMAGES_DIR = "data/test_images"

# 测试URL
TEST_URL = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhogfq9bf86q"

# 文档ID映射表
DOC_ID_MAP_FILE = "data/doc_id_map.json"

# 加载文档ID映射表
def load_doc_id_map():
    try:
        with open(DOC_ID_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load doc_id_map: {e}")
        return {}

# 执行完整爬虫测试
def run_crawler_test():
    """运行完整的爬虫测试，包括爬取、解析、下载和链接替换"""
    import sys
    import os
    
    # 确保项目根目录在Python路径中
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.crawler.spider import Spider
    from src.crawler.parser import Parser
    from src.crawler.downloader import Downloader
    
    # 初始化爬虫组件
    spider = Spider()
    parser = Parser()
    downloader = Downloader()
    
    # 加载文档ID映射表
    doc_id_map = load_doc_id_map()
    
    # 爬取测试页面
    print(f"\n正在爬取测试页面: {TEST_URL}")
    page_content = spider.get_page(TEST_URL)
    
    if not page_content:
        print("✗ 爬取页面失败")
        return None
    
    # 提取文档ID
    doc_id = TEST_URL.split('/')[-1]
    title = doc_id_map.get(doc_id, doc_id)
    
    # 解析页面内容
    parsed_content = parser.parse_content(page_content)
    if not parsed_content:
        print("✗ 解析页面内容失败")
        return None
    
    # 解析页面中的图片
    images = parser.parse_images(page_content)
    print(f"✓ 发现 {len(images)} 个图片")
    
    # 在测试目录保存Markdown文件
    test_filename = f"{title}_{doc_id[:8]}_test.md"
    test_filepath = os.path.join(TEST_MARKDOWN_DIR, test_filename)
    
    # 保存初始Markdown文件
    with open(test_filepath, 'w', encoding='utf-8') as f:
        f.write(parsed_content['content'])
    
    # 下载图片并记录映射关系
    img_map = {}
    for img_url in images:
        downloaded_filename = downloader.download_image(img_url, TEST_IMAGES_DIR)
        if downloaded_filename:
            img_map[img_url] = downloaded_filename
            print(f"✓ 下载图片成功: {downloaded_filename}")
        else:
            print(f"✗ 下载图片失败: {img_url}")
    
    # 读取保存的Markdown文件
    with open(test_filepath, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # 替换图片链接
    if img_map:
        for img_url, local_filename in img_map.items():
            # 创建本地相对路径
            local_path = f"../test_images/{local_filename}"
            # 替换CDN链接为本地相对路径
            markdown_content = markdown_content.replace(f"![]({img_url})", f"![]({local_path})")
            # 替换空图片链接
            markdown_content = markdown_content.replace("![]()", f"![]({local_path})")
    
    # 解析页面中的链接
    links = parser.parse_links(page_content, TEST_URL)
    print(f"✓ 发现 {len(links)} 个链接")
    
    # 替换本地跳转链接
    if links:
        import re
        for link in links:
            # 提取文档ID
            link_doc_id = link.split('/')[-1]
            # 查找对应的本地文件名
            if link_doc_id in doc_id_map:
                link_title = doc_id_map[link_doc_id]
                local_filename = f"{link_title}_{link_doc_id[:8]}.md"
                # 创建本地相对路径
                local_path = f"./{local_filename}"
                
                # 提取基本URL部分，用于匹配不同格式的链接
                base_url = "/ys/ugc/tutorial/detail/"
                relative_link1 = f"/ys/ugc/tutorial//detail/{link_doc_id}"
                relative_link2 = f"{base_url}{link_doc_id}"
                
                # 使用正则表达式替换所有包含该链接的Markdown链接，无论链接文本是什么
                for url_pattern in [link, relative_link1, relative_link2]:
                    # 转义URL中的特殊字符，用于正则表达式
                    escaped_url = re.escape(url_pattern)
                    # 匹配Markdown链接格式：[任意文本](URL)
                    link_pattern = re.compile(r'\[([^\]]+)\]\(\s*' + escaped_url + r'\s*\)')
                    # 替换为本地链接
                    markdown_content = link_pattern.sub(rf'[\1]({local_path})', markdown_content)
    
    # 保存更新后的Markdown文件
    with open(test_filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✓ 完整爬虫流程测试完成，测试文件已保存到: {test_filepath}")
    
    # 返回处理后的内容
    return markdown_content

# 测试空图片链接修复
def test_empty_image_links(content):
    """测试空图片链接是否已修复"""
    # 查找所有空图片链接
    empty_img_pattern = r'!\[\]\(\)'
    empty_img_matches = re.findall(empty_img_pattern, content)
    
    if not empty_img_matches:
        return True, "✓ 空图片链接已修复，未发现空图片链接"
    else:
        return False, f"✗ 仍存在空图片链接，共 {len(empty_img_matches)} 个"

# 测试自定义列表修复
def test_custom_lists(content):
    """测试自定义列表是否已修复"""
    # 查找所有自定义列表标记
    custom_list_marker = r''
    custom_list_matches = re.findall(custom_list_marker, content)
    
    if not custom_list_matches:
        # 查找标准Markdown列表
        standard_list_pattern = r'^[\s]*[-*+]\s+'
        standard_list_matches = re.findall(standard_list_pattern, content, re.MULTILINE)
        if standard_list_matches:
            return True, f"✓ 自定义列表已修复，共发现 {len(standard_list_matches)} 个标准列表项"
        else:
            return True, "✓ 自定义列表已修复，未发现自定义列表标记"
    else:
        return False, f"✗ 仍存在自定义列表标记，共 {len(custom_list_matches)} 个"

# 测试图片链接本地化
def test_image_link_localization(content):
    """测试图片链接是否已转换为本地路径"""
    # 查找所有图片链接
    img_pattern = r'!\[.*?\]\((.*?)\)'
    img_matches = re.findall(img_pattern, content)
    
    cdn_links = []
    local_links = []
    
    for img_url in img_matches:
        if img_url.startswith("http"):
            cdn_links.append(img_url)
        elif img_url.startswith("../images/"):
            local_links.append(img_url)
    
    if not cdn_links:
        return True, f"✓ 图片链接已本地化，共 {len(local_links)} 个本地图片链接"
    else:
        return False, f"✗ 仍存在CDN图片链接，共 {len(cdn_links)} 个CDN链接，{len(local_links)} 个本地链接"

# 测试链接本地化
def test_link_localization(content, doc_id_map):
    """测试链接是否已转换为本地文件路径"""
    # 查找所有Markdown链接
    link_pattern = r'\[.*?\]\((.*?)\)'
    link_matches = re.findall(link_pattern, content)
    
    external_links = []
    local_links = []
    
    for link in link_matches:
        if link.startswith("http") or link.startswith("/ys/ugc/tutorial"):
            external_links.append(link)
        elif link.endswith(".md"):
            local_links.append(link)
    
    if not external_links:
        return True, f"✓ 链接已本地化，共 {len(local_links)} 个本地链接"
    else:
        # 打印具体的外部链接，用于调试
        print(f"\n调试信息：未本地化的外部链接：")
        for link in external_links:
            print(f"  - {link}")
        return False, f"✗ 仍存在外部链接，共 {len(external_links)} 个外部链接，{len(local_links)} 个本地链接"

# 主测试函数
def main():
    print("=" * 60)
    print("测试修复效果")
    print("=" * 60)
    
    # 运行爬虫测试，获取修复后的内容
    content = run_crawler_test()
    
    if not content:
        print("\n❌ 无法获取测试内容，测试失败。")
        return False
    
    # 加载文档ID映射表
    doc_id_map = load_doc_id_map()
    
    # 运行所有测试
    tests = [
        ("空图片链接修复", test_empty_image_links, [content]),
        ("自定义列表修复", test_custom_lists, [content]),
        ("图片链接本地化", test_image_link_localization, [content]),
        ("链接本地化", test_link_localization, [content, doc_id_map])
    ]
    
    # 保存测试结果
    results = []
    all_passed = True
    
    for test_name, test_func, args in tests:
        print(f"\n测试项: {test_name}")
        print("-" * 40)
        
        success, message = test_func(*args)
        print(message)
        
        results.append({
            "test_name": test_name,
            "success": success,
            "message": message
        })
        
        if not success:
            all_passed = False
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for result in results:
        status = "✓" if result["success"] else "✗"
        print(f"{status} {result['test_name']}: {result['message']}")
    
    print("\n" + "=" * 60)
    print("最终结论")
    print("=" * 60)
    
    # 保存测试报告
    save_test_report(results, all_passed, content)
    
    if all_passed:
        print("🎉 所有修复项均已通过测试！")
    else:
        print("❌ 部分修复项未通过测试，需要进一步调试。")
    
    return all_passed

# 保存测试报告
def save_test_report(results, all_passed, content):
    """保存测试报告到文件"""
    from datetime import datetime
    
    # 生成报告文件名
    report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{report_time}.md"
    
    # 生成报告内容
    report = f"# 修复效果测试报告\n\n"
    report += f"## 测试基本信息\n"
    report += f"- 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"- 测试URL: {TEST_URL}\n"
    report += f"- 测试结果: {'通过' if all_passed else '未通过'}\n\n"
    
    report += f"## 测试项结果\n"
    for result in results:
        status = "✅" if result["success"] else "❌"
        report += f"- {status} {result['test_name']}: {result['message']}\n"
    
    report += f"\n## 测试内容摘要\n"
    # 提取前500个字符作为摘要
    content_summary = content[:500] + "..." if len(content) > 500 else content
    report += f"```markdown\n{content_summary}\n```\n"
    
    # 保存报告
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 测试报告已保存到: {report_file}")

if __name__ == "__main__":
    main()
