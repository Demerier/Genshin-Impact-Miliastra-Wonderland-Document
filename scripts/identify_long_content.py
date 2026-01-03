#!/usr/bin/env python3
"""
识别极长内容文档的脚本
"""

import os
import sys

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import logger

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
# Markdown保存目录
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
# 极长内容阈值（字符数）
LONG_CONTENT_THRESHOLD = 500000

def identify_long_content():
    """识别极长内容文档"""
    logger.info(f"开始识别极长内容文档，阈值: {LONG_CONTENT_THRESHOLD} 字符")
    
    # 获取所有Markdown文件
    markdown_files = []
    for root, _, files in os.walk(MARKDOWN_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                markdown_files.append(file_path)
    
    logger.info(f"共找到 {len(markdown_files)} 个Markdown文件")
    
    # 检查文件大小
    long_content_files = []
    file_stats = []
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            char_count = len(content)
            
            # 记录文件统计信息
            file_stats.append({
                "file_path": file_path,
                "filename": os.path.basename(file_path),
                "char_count": char_count,
                "is_long": char_count > LONG_CONTENT_THRESHOLD
            })
            
            # 检查是否为极长内容
            if char_count > LONG_CONTENT_THRESHOLD:
                long_content_files.append(file_path)
                logger.info(f"发现极长内容文档: {os.path.basename(file_path)} ({char_count:,} 字符)")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 时出错: {e}")
    
    # 按字符数降序排序
    file_stats.sort(key=lambda x: x["char_count"], reverse=True)
    
    # 生成统计报告
    generate_statistics_report(file_stats, long_content_files)
    
    return long_content_files

def generate_statistics_report(file_stats, long_content_files):
    """生成统计报告"""
    from datetime import datetime
    
    report = f"# 极长内容文档识别报告\n\n"
    report += f"## 基本信息\n"
    report += f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"- 极长内容阈值: {LONG_CONTENT_THRESHOLD:,} 字符\n"
    report += f"- 总文档数: {len(file_stats)}\n"
    report += f"- 极长内容文档数: {len(long_content_files)}\n"
    report += f"- 极长内容比例: {len(long_content_files) / len(file_stats) * 100:.2f}%\n\n"
    
    report += f"## 极长内容文档列表\n"
    if long_content_files:
        for file_path in long_content_files:
            filename = os.path.basename(file_path)
            stat = next(s for s in file_stats if s["filename"] == filename)
            report += f"- {filename}: {stat['char_count']:,} 字符\n"
    else:
        report += f"- 未发现极长内容文档\n"
    
    report += f"\n## 文档大小排名前20\n"
    for i, stat in enumerate(file_stats[:20], 1):
        report += f"{i}. {stat['filename']}: {stat['char_count']:,} 字符"
        if stat["is_long"]:
            report += " (极长内容)"
        report += "\n"
    
    # 保存报告
    report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "reports", "long_content_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"极长内容识别报告已保存到: {report_path}")
    
    # 保存极长内容文件列表
    long_content_list_path = os.path.join(DATA_DIR, "processed", "long_content_files.txt")
    with open(long_content_list_path, 'w', encoding='utf-8') as f:
        for file_path in long_content_files:
            f.write(f"{file_path}\n")
    
    logger.info(f"极长内容文件列表已保存到: {long_content_list_path}")
    
    return report

def main():
    """主函数"""
    logger.info("开始识别极长内容文档...")
    long_content_files = identify_long_content()
    
    if long_content_files:
        logger.info(f"共发现 {len(long_content_files)} 个极长内容文档")
    else:
        logger.info("未发现极长内容文档")

if __name__ == "__main__":
    main()
