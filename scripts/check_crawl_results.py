#!/usr/bin/env python3
"""
爬取结果初步检查脚本
"""

import os
import sys
import re

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import logger

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
# Markdown保存目录
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
# 图片保存目录
IMAGES_DIR = os.path.join(DATA_DIR, "images")

# 预期文档数量（根据初始数据采集结果）
EXPECTED_DOC_COUNT = 144

def check_crawl_results():
    """进行爬取结果初步检查"""
    logger.info("开始进行爬取结果初步检查...")
    
    # 初始化检查结果
    check_results = {
        "total_docs": 0,
        "expected_docs": EXPECTED_DOC_COUNT,
        "missing_docs": 0,
        "valid_filenames": 0,
        "invalid_filenames": 0,
        "empty_files": 0,
        "valid_format": 0,
        "invalid_format": 0,
        "average_content_length": 0,
        "total_images": 0,
        "broken_image_links": 0,
        "issues": []
    }
    
    # 获取所有Markdown文件
    markdown_files = []
    for root, _, files in os.walk(MARKDOWN_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                markdown_files.append(file_path)
    
    check_results["total_docs"] = len(markdown_files)
    
    # 检查文档数量
    if len(markdown_files) != EXPECTED_DOC_COUNT:
        check_results["missing_docs"] = abs(len(markdown_files) - EXPECTED_DOC_COUNT)
        check_results["issues"].append({
            "type": "数量不匹配",
            "message": f"实际文档数 {len(markdown_files)} 与预期 {EXPECTED_DOC_COUNT} 不符，相差 {check_results['missing_docs']} 个"
        })
    else:
        logger.info(f"文档数量检查通过: {len(markdown_files)} 个文档")
    
    # 检查每个文件
    total_char_count = 0
    
    for file_path in markdown_files:
        filename = os.path.basename(file_path)
        
        # 1. 检查文件名规范
        # 允许中文、英文、数字、下划线、连字符
        if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\-]+\.md$', filename):
            check_results["valid_filenames"] += 1
        else:
            check_results["invalid_filenames"] += 1
            check_results["issues"].append({
                "type": "文件名不规范",
                "message": f"文件名 {filename} 不符合规范"
            })
        
        try:
            # 2. 检查文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            char_count = len(content)
            total_char_count += char_count
            
            # 3. 检查是否为空文件
            if char_count == 0:
                check_results["empty_files"] += 1
                check_results["issues"].append({
                    "type": "空文件",
                    "message": f"文件 {filename} 内容为空"
                })
            
            # 4. 检查格式有效性（简单检查）
            # 检查是否包含基本的Markdown格式元素
            has_valid_format = any([
                content.strip().startswith('#'),  # 包含标题
                '![alt]' in content,  # 包含图片
                '[text](' in content,  # 包含链接
                '```' in content,  # 包含代码块
                '- ' in content or '* ' in content or '1. ' in content  # 包含列表
            ]) or char_count > 100  # 或者内容较长
            
            if has_valid_format:
                check_results["valid_format"] += 1
            else:
                check_results["invalid_format"] += 1
                check_results["issues"].append({
                    "type": "格式可能无效",
                    "message": f"文件 {filename} 可能缺少有效的Markdown格式"
                })
            
            # 5. 检查图片链接有效性
            # 查找所有图片链接
            image_links = re.findall(r'!\[.*?\]\((.*?)\)', content)
            check_results["total_images"] += len(image_links)
            
            for img_link in image_links:
                # 检查本地图片链接
                if img_link.startswith('./images/'):
                    # 获取图片文件名
                    img_filename = img_link.split('/')[-1]
                    img_path = os.path.join(IMAGES_DIR, img_filename)
                    if not os.path.exists(img_path):
                        check_results["broken_image_links"] += 1
                        check_results["issues"].append({
                            "type": "图片链接无效",
                            "message": f"文件 {filename} 中的图片链接 {img_link} 指向不存在的文件"
                        })
                    
        except Exception as e:
            check_results["issues"].append({
                "type": "文件读取错误",
                "message": f"处理文件 {filename} 时出错: {e}"
            })
    
    # 计算平均内容长度
    if check_results["total_docs"] > 0:
        check_results["average_content_length"] = total_char_count / check_results["total_docs"]
    
    # 生成检查报告
    generate_check_report(check_results)
    
    return check_results

def generate_check_report(check_results):
    """生成检查报告"""
    from datetime import datetime
    
    report = f"# 爬取结果初步检查报告\n\n"
    report += f"## 基本信息\n"
    report += f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"- 检查目录: {MARKDOWN_DIR}\n\n"
    
    report += f"## 检查结果\n"
    report += f"| 检查项 | 预期值 | 实际值 | 状态 |\n"
    report += f"|--------|--------|--------|------|\n"
    
    # 文档数量
    doc_count_status = "✅ 通过" if check_results["total_docs"] == check_results["expected_docs"] else "❌ 不通过"
    report += f"| 文档数量 | {check_results['expected_docs']} | {check_results['total_docs']} | {doc_count_status} |\n"
    
    # 文件名规范
    filename_status = "✅ 通过" if check_results["invalid_filenames"] == 0 else "⚠️  部分不通过"
    report += f"| 文件名规范 | 100% | {check_results['valid_filenames'] / check_results['total_docs'] * 100:.1f}% | {filename_status} |\n"
    
    # 空文件检查
    empty_status = "✅ 通过" if check_results["empty_files"] == 0 else "⚠️  部分不通过"
    report += f"| 空文件检查 | 0 | {check_results['empty_files']} | {empty_status} |\n"
    
    # 格式有效性
    format_status = "✅ 通过" if check_results["invalid_format"] == 0 else "⚠️  部分不通过"
    report += f"| 格式有效性 | 100% | {check_results['valid_format'] / check_results['total_docs'] * 100:.1f}% | {format_status} |\n"
    
    # 图片链接有效性
    image_status = "✅ 通过" if check_results["broken_image_links"] == 0 else "⚠️  部分不通过"
    report += f"| 图片链接有效性 | 0 | {check_results['broken_image_links']} | {image_status} |\n"
    
    report += f"\n## 内容统计\n"
    report += f"- 平均内容长度: {check_results['average_content_length']:.0f} 字符\n"
    report += f"- 总图片链接数: {check_results['total_images']}\n"
    report += f"- 无效图片链接数: {check_results['broken_image_links']}\n"
    
    if check_results["issues"]:
        report += f"\n## 问题列表\n"
        for issue in check_results["issues"]:
            report += f"- **{issue['type']}**: {issue['message']}\n"
    else:
        report += f"\n## 问题列表\n"
        report += f"- 未发现明显问题\n"
    
    # 保存报告
    report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "reports", "crawl_check_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"爬取结果初步检查报告已保存到: {report_path}")
    
    # 打印摘要
    logger.info("\n===== 爬取结果初步检查摘要 =====")
    logger.info(f"文档数量: {check_results['total_docs']} / {check_results['expected_docs']}")
    logger.info(f"文件名规范: {check_results['valid_filenames']}/{check_results['total_docs']} 有效")
    logger.info(f"空文件: {check_results['empty_files']} 个")
    logger.info(f"格式有效: {check_results['valid_format']}/{check_results['total_docs']}")
    logger.info(f"平均内容长度: {check_results['average_content_length']:.0f} 字符")
    logger.info(f"图片链接: {check_results['total_images']} 个，其中 {check_results['broken_image_links']} 个无效")
    
    if check_results["issues"]:
        logger.warning(f"共发现 {len(check_results['issues'])} 个问题")
    else:
        logger.info("未发现明显问题")
    
    return report

def main():
    """主函数"""
    check_results = check_crawl_results()
    
    # 根据检查结果决定是否通过
    if len(check_results["issues"]) == 0:
        logger.info("爬取结果初步检查通过！")
        return 0
    else:
        logger.warning(f"爬取结果初步检查发现 {len(check_results['issues'])} 个问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())
