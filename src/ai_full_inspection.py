#!/usr/bin/env python3
"""
AI全面自检脚本
"""

import os
import sys
import json
import re

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import logger

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
# Markdown保存目录
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
# 文档ID映射表文件路径
DOC_ID_MAP_FILE = os.path.join(DATA_DIR, "doc_id_map.json")
# URL列表文件路径
URL_LIST_FILE = os.path.join(DATA_DIR, "url_list.txt")

# 预期文档数量
EXPECTED_DOC_COUNT = 144

def ai_full_inspection():
    """执行AI全面自检"""
    logger.info("开始执行AI全面自检...")
    
    # 加载文档ID映射表
    doc_id_map = load_doc_id_map()
    
    # 加载URL列表
    url_list = load_url_list()
    
    # 获取实际爬取的文件
    actual_files = get_actual_files()
    
    # 初始化自检结果
    inspection_results = {
        "total_expected": EXPECTED_DOC_COUNT,
        "total_actual": len(actual_files),
        "issues": [],
        "missing_docs": [],
        "invalid_filenames": [],
        "empty_files": [],
        "invalid_format_files": [],
        "quality_score": 0
    }
    
    # 1. 检查文档数量和缺少的文档
    logger.info("检查文档数量和缺少的文档...")
    check_missing_docs(doc_id_map, actual_files, inspection_results)
    
    # 2. 检查文件名规范
    logger.info("检查文件名规范...")
    check_filename规范(actual_files, inspection_results)
    
    # 3. 检查空文件
    logger.info("检查空文件...")
    check_empty_files(actual_files, inspection_results)
    
    # 4. 检查格式有效性和内容质量
    logger.info("检查格式有效性和内容质量...")
    check_format_and_quality(actual_files, inspection_results)
    
    # 5. 计算质量评分
    calculate_quality_score(inspection_results)
    
    # 6. 生成自检报告
    generate_inspection_report(inspection_results)
    
    return inspection_results

def load_doc_id_map():
    """加载文档ID映射表"""
    try:
        with open(DOC_ID_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load doc_id_map: {e}")
        return {}

def load_url_list():
    """加载URL列表"""
    urls = []
    try:
        with open(URL_LIST_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url:
                    urls.append(url)
    except Exception as e:
        logger.error(f"Failed to load url_list: {e}")
    return urls

def get_actual_files():
    """获取实际爬取的文件"""
    actual_files = []
    for root, _, files in os.walk(MARKDOWN_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                actual_files.append({
                    "file_path": file_path,
                    "filename": file,
                    "title": file[:-3]  # 去掉.md后缀
                })
    return actual_files

def check_missing_docs(doc_id_map, actual_files, results):
    """检查缺少的文档"""
    # 获取实际文件名集合（不含.md后缀）
    actual_titles = set(file["title"] for file in actual_files)
    
    # 检查每个预期文档
    for doc_id, expected_title in doc_id_map.items():
        if expected_title not in actual_titles:
            # 检查是否有近似匹配（容错）
            found = False
            for actual_title in actual_titles:
                if expected_title in actual_title or actual_title in expected_title:
                    found = True
                    break
            
            if not found:
                results["missing_docs"].append({
                    "doc_id": doc_id,
                    "expected_title": expected_title,
                    "url": f"https://act.mihoyo.com/ys/ugc/tutorial/detail/{doc_id}"
                })
    
    if results["missing_docs"]:
        results["issues"].append({
            "type": "missing_docs",
            "count": len(results["missing_docs"]),
            "message": f"缺少 {len(results['missing_docs'])} 个文档",
            "details": results["missing_docs"]
        })

def check_filename规范(actual_files, results):
    """检查文件名规范"""
    for file in actual_files:
        filename = file["filename"]
        # 允许中文、英文、数字、下划线、连字符
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\-]+\.md$', filename):
            results["invalid_filenames"].append({
                "file_path": file["file_path"],
                "filename": filename,
                "issue": "文件名包含非法字符"
            })
    
    if results["invalid_filenames"]:
        results["issues"].append({
            "type": "invalid_filenames",
            "count": len(results["invalid_filenames"]),
            "message": f"{len(results['invalid_filenames'])} 个文件名不符合规范",
            "details": results["invalid_filenames"]
        })

def check_empty_files(actual_files, results):
    """检查空文件"""
    for file in actual_files:
        try:
            with open(file["file_path"], 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) == 0:
                results["empty_files"].append({
                    "file_path": file["file_path"],
                    "filename": file["filename"]
                })
        except Exception as e:
            results["issues"].append({
                "type": "file_read_error",
                "count": 1,
                "message": f"读取文件 {file['filename']} 时出错: {e}"
            })
    
    if results["empty_files"]:
        results["issues"].append({
            "type": "empty_files",
            "count": len(results["empty_files"]),
            "message": f"{len(results['empty_files'])} 个文件内容为空",
            "details": results["empty_files"]
        })

def check_format_and_quality(actual_files, results):
    """检查格式有效性和内容质量"""
    for file in actual_files:
        try:
            with open(file["file_path"], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 跳过空文件（已经在前面检查过）
            if len(content) == 0:
                continue
            
            # 检查格式有效性
            format_score = evaluate_format(content)
            
            # 检查内容质量
            content_score = evaluate_content(content)
            
            # 综合质量评分
            file_score = (format_score + content_score) / 2
            
            # 如果质量评分低于阈值，记录为问题文件
            if file_score < 70:
                results["invalid_format_files"].append({
                    "file_path": file["file_path"],
                    "filename": file["filename"],
                    "format_score": format_score,
                    "content_score": content_score,
                    "file_score": file_score,
                    "issues": []
                })
                
                # 详细分析问题
                analyze_file_issues(content, results["invalid_format_files"][-1])
        
        except Exception as e:
            results["issues"].append({
                "type": "file_read_error",
                "count": 1,
                "message": f"读取文件 {file['filename']} 时出错: {e}"
            })
    
    if results["invalid_format_files"]:
        results["issues"].append({
            "type": "invalid_format_quality",
            "count": len(results["invalid_format_files"]),
            "message": f"{len(results['invalid_format_files'])} 个文件格式或内容质量不佳",
            "details": results["invalid_format_files"]
        })

def evaluate_format(content):
    """评估文件格式质量"""
    score = 100
    
    # 检查基本格式元素
    has_heading = content.strip().startswith('#')
    has_paragraph = len(content.split('\n\n')) > 1
    has_valid_markdown = any([
        '![alt]' in content,  # 图片
        '[text](' in content,  # 链接
        '```' in content,  # 代码块
        '- ' in content or '* ' in content or '1. ' in content  # 列表
    ])
    
    # 基于格式元素扣分
    if not has_heading:
        score -= 20
    if not has_paragraph and len(content) < 200:
        score -= 15
    if not has_valid_markdown and len(content) < 100:
        score -= 10
    
    # 检查是否有异常格式
    if '\r\n\r\n\r\n' in content:  # 过多空行
        score -= 5
    if '#######' in content:  # 无效标题级别
        score -= 10
    
    return max(0, min(100, score))

def evaluate_content(content):
    """评估内容质量"""
    score = 100
    
    # 内容长度评分
    content_length = len(content)
    if content_length < 50:
        score -= 30
    elif content_length < 100:
        score -= 20
    elif content_length < 200:
        score -= 10
    
    # 检查内容完整性
    if '...' in content[-10:]:  # 内容可能被截断
        score -= 20
    
    # 检查内容可读性
    lines = [line for line in content.split('\n') if line.strip()]
    if len(lines) < 3:
        score -= 15
    
    # 检查是否有重复内容
    if len(content) > 100:
        # 简单检查是否有大段重复
        for i in range(0, len(content), 50):
            chunk = content[i:i+50]
            if content.count(chunk) > 3:
                score -= 10
                break
    
    return max(0, min(100, score))

def analyze_file_issues(content, file_result):
    """分析文件问题"""
    issues = []
    
    # 检查问题
    if len(content) < 50:
        issues.append("内容过短")
    if not content.strip().startswith('#'):
        issues.append("缺少标题")
    if '\r\n\r\n\r\n' in content:
        issues.append("过多空行")
    if '#######' in content:
        issues.append("无效标题级别")
    if '...' in content[-10:]:
        issues.append("内容可能被截断")
    
    file_result["issues"] = issues

def calculate_quality_score(results):
    """计算整体质量评分"""
    # 基础评分
    base_score = 100
    
    # 根据问题扣分
    if results["missing_docs"]:
        # 每个缺少的文档扣1分
        base_score -= min(20, len(results["missing_docs"]))
    
    if results["invalid_filenames"]:
        # 每个无效文件名扣0.5分
        base_score -= min(5, len(results["invalid_filenames"]) * 0.5)
    
    if results["empty_files"]:
        # 每个空文件扣5分
        base_score -= min(20, len(results["empty_files"]) * 5)
    
    if results["invalid_format_files"]:
        # 每个无效格式文件扣1分
        base_score -= min(30, len(results["invalid_format_files"]))
    
    # 确保评分在0-100之间
    results["quality_score"] = max(0, min(100, base_score))

def generate_inspection_report(results):
    """生成自检报告"""
    from datetime import datetime
    
    report = f"# AI全面自检报告\n\n"
    report += f"## 基本信息\n"
    report += f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"- 预期文档数量: {results['total_expected']}\n"
    report += f"- 实际文档数量: {results['total_actual']}\n"
    report += f"- 整体质量评分: {results['quality_score']:.1f} / 100\n\n"
    
    # 评分等级
    if results["quality_score"] >= 90:
        report += f"- 评分等级: ✅ 优秀\n\n"
    elif results["quality_score"] >= 80:
        report += f"- 评分等级: ✅ 良好\n\n"
    elif results["quality_score"] >= 70:
        report += f"- 评分等级: ⚠️  合格\n\n"
    else:
        report += f"- 评分等级: ❌ 不合格\n\n"
    
    report += f"## 问题汇总\n"
    report += f"| 问题类型 | 数量 | 详情 |\n"
    report += f"|----------|------|------|\n"
    
    # 缺少的文档
    if results["missing_docs"]:
        report += f"| 缺少文档 | {len(results['missing_docs'])} | 缺少 {len(results['missing_docs'])} 个文档 |\n"
    
    # 无效文件名
    if results["invalid_filenames"]:
        report += f"| 无效文件名 | {len(results['invalid_filenames'])} | {len(results['invalid_filenames'])} 个文件名不符合规范 |\n"
    
    # 空文件
    if results["empty_files"]:
        report += f"| 空文件 | {len(results['empty_files'])} | {len(results['empty_files'])} 个文件内容为空 |\n"
    
    # 格式质量问题
    if results["invalid_format_files"]:
        report += f"| 格式质量问题 | {len(results['invalid_format_files'])} | {len(results['invalid_format_files'])} 个文件格式或内容质量不佳 |\n"
    
    report += f"\n## 详细问题列表\n"
    
    # 缺少的文档详细信息
    if results["missing_docs"]:
        report += f"### 缺少的文档\n"
        for doc in results["missing_docs"]:
            report += f"- **{doc['expected_title']}**\n  - 文档ID: {doc['doc_id']}\n  - URL: {doc['url']}\n"
        report += f"\n"
    
    # 无效文件名详细信息
    if results["invalid_filenames"]:
        report += f"### 无效文件名\n"
        for file in results["invalid_filenames"]:
            report += f"- {file['filename']}: {file['issue']}\n"
        report += f"\n"
    
    # 空文件详细信息
    if results["empty_files"]:
        report += f"### 空文件\n"
        for file in results["empty_files"]:
            report += f"- {file['filename']}\n"
        report += f"\n"
    
    # 格式质量问题详细信息
    if results["invalid_format_files"]:
        report += f"### 格式质量问题文件\n"
        report += f"| 文件名 | 格式评分 | 内容评分 | 综合评分 | 问题 |\n"
        report += f"|--------|----------|----------|----------|------|\n"
        for file in results["invalid_format_files"]:
            issues = ", ".join(file["issues"]) if file["issues"] else "无详细问题"
            report += f"| {file['filename']} | {file['format_score']:.1f} | {file['content_score']:.1f} | {file['file_score']:.1f} | {issues} |\n"
        report += f"\n"
    
    # 修复建议
    report += f"## 修复建议\n"
    
    if results["missing_docs"]:
        report += f"1. **缺少文档**：建议重新爬取缺少的 {len(results['missing_docs'])} 个文档，检查爬取逻辑是否存在问题。\n"
    
    if results["invalid_filenames"]:
        report += f"2. **无效文件名**：建议重命名不符合规范的文件名，确保只包含中文、英文、数字、下划线和连字符。\n"
    
    if results["empty_files"]:
        report += f"3. **空文件**：建议重新爬取这些空文件，检查爬取时是否遇到了网络问题或反爬机制。\n"
    
    if results["invalid_format_files"]:
        report += f"4. **格式质量问题**：建议对这些文件进行手动检查和修复，重点关注内容完整性和格式规范性。\n"
    
    # 整体评估
    if results["quality_score"] >= 90:
        report += f"\n## 整体评估\n"
        report += f"✅ 爬取结果质量优秀，符合预期要求，可以进行后续处理和交付。\n"
    elif results["quality_score"] >= 80:
        report += f"\n## 整体评估\n"
        report += f"✅ 爬取结果质量良好，存在少量问题，建议进行简单修复后交付。\n"
    elif results["quality_score"] >= 70:
        report += f"\n## 整体评估\n"
        report += f"⚠️  爬取结果质量合格，但存在一些问题，建议进行必要的修复后再交付。\n"
    else:
        report += f"\n## 整体评估\n"
        report += f"❌ 爬取结果质量不合格，存在较多问题，建议进行全面修复或重新爬取。\n"
    
    # 保存报告
    report_path = os.path.join(DATA_DIR, "ai_inspection_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"AI全面自检报告已保存到: {report_path}")
    
    # 打印报告摘要
    logger.info("\n===== AI全面自检报告摘要 =====")
    logger.info(f"整体质量评分: {results['quality_score']:.1f} / 100")
    logger.info(f"缺少文档: {len(results['missing_docs'])} 个")
    logger.info(f"无效文件名: {len(results['invalid_filenames'])} 个")
    logger.info(f"空文件: {len(results['empty_files'])} 个")
    logger.info(f"格式质量问题: {len(results['invalid_format_files'])} 个")
    
    if results["quality_score"] >= 80:
        logger.info("✅ 爬取结果整体质量良好，符合预期要求")
    else:
        logger.warning("⚠️  爬取结果存在一些问题，建议进行修复")

def main():
    """主函数"""
    ai_full_inspection()

if __name__ == "__main__":
    main()
