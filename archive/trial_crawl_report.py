#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
试行爬取报告生成器
负责生成详细的试行爬取报告，包括统计结果、问题分析和解决方案建议
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Issue:
    """问题描述"""
    severity: str
    category: str
    description: str
    affected_pages: List[str]
    suggested_solution: str


@dataclass
class Recommendation:
    """建议"""
    priority: str
    category: str
    description: str
    rationale: str


class TrialCrawlReportGenerator:
    """试行爬取报告生成器"""
    
    def __init__(self, monitor, config, logger=None):
        """初始化报告生成器
        
        Args:
            monitor: 监控器对象
            config: 配置对象
            logger: 日志记录器
        """
        self.monitor = monitor
        self.config = config
        self.logger = logger
        
        self.output_dir = Path(config.log_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.issues: List[Issue] = []
        self.recommendations: List[Recommendation] = []
    
    def analyze_results(self):
        """分析爬取结果，识别问题和改进点"""
        self.logger.info("开始分析爬取结果...")
        
        summary = self.monitor.get_summary()
        page_details = self.monitor.get_page_details()
        
        # 分析成功率
        success_rate = summary["crawl_summary"]["success_rate_percent"]
        if success_rate < 100:
            self._analyze_failures(page_details)
        
        # 分析性能
        avg_load_time = summary["performance_metrics"]["average_load_time_seconds"]
        if avg_load_time > 10:
            self._analyze_performance(page_details, avg_load_time)
        
        # 分析内容提取
        avg_content_length = summary["performance_metrics"]["average_content_length"]
        if avg_content_length < 500:
            self._analyze_content_extraction(page_details, avg_content_length)
        
        # 分析资源下载
        total_images = summary["resource_metrics"]["total_images_downloaded"]
        if total_images == 0:
            self._analyze_image_download(page_details)
        
        # 分析重试和错误
        total_retries = summary["crawl_summary"]["total_retries"]
        total_errors = summary["crawl_summary"]["total_errors"]
        if total_retries > 0 or total_errors > 0:
            self._analyze_errors(page_details, total_retries, total_errors)
        
        # 生成建议
        self._generate_recommendations(summary)
        
        self.logger.info(f"分析完成，发现 {len(self.issues)} 个问题，{len(self.recommendations)} 条建议")
    
    def _analyze_failures(self, page_details: List[Dict[str, Any]]):
        """分析失败页面"""
        failed_pages = [p for p in page_details if not p.get('is_success', False)]
        
        if failed_pages:
            error_types = {}
            for page in failed_pages:
                error_type = page.get('error_type', 'Unknown')
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            most_common_error = max(error_types.items(), key=lambda x: x[1])[0]
            
            issue = Issue(
                severity="high",
                category="爬取失败",
                description=f"发现 {len(failed_pages)} 个页面爬取失败，主要错误类型: {most_common_error}",
                affected_pages=[p['name'] for p in failed_pages],
                suggested_solution="检查网络连接、目标网站可访问性，或增加重试次数和超时时间"
            )
            self.issues.append(issue)
    
    def _analyze_performance(self, page_details: List[Dict[str, Any]], avg_load_time: float):
        """分析性能问题"""
        slow_pages = [p for p in page_details if p.get('load_time', 0) > avg_load_time * 1.5]
        
        if slow_pages:
            issue = Issue(
                severity="medium",
                category="性能问题",
                description=f"平均加载时间 {avg_load_time:.2f} 秒，{len(slow_pages)} 个页面加载较慢",
                affected_pages=[p['name'] for p in slow_pages],
                suggested_solution="优化等待策略，减少不必要的等待时间，或考虑使用更轻量级的浏览器配置"
            )
            self.issues.append(issue)
    
    def _analyze_content_extraction(self, page_details: List[Dict[str, Any]], avg_content_length: float):
        """分析内容提取问题"""
        low_content_pages = [p for p in page_details if p.get('content_length', 0) < avg_content_length * 0.5]
        
        if low_content_pages:
            issue = Issue(
                severity="medium",
                category="内容提取",
                description=f"平均内容长度 {avg_content_length:.0f} 字符，{len(low_content_pages)} 个页面内容较少",
                affected_pages=[p['name'] for p in low_content_pages],
                suggested_solution="检查页面解析规则，确保选择器正确匹配内容区域，或调整最小内容长度阈值"
            )
            self.issues.append(issue)
    
    def _analyze_image_download(self, page_details: List[Dict[str, Any]]):
        """分析图片下载问题"""
        pages_with_images = [p for p in page_details if p.get('image_count', 0) > 0]
        
        if pages_with_images:
            issue = Issue(
                severity="low",
                category="图片下载",
                description=f"{len(pages_with_images)} 个页面包含图片但未成功下载",
                affected_pages=[p['name'] for p in pages_with_images],
                suggested_solution="检查图片URL有效性、网络连接，或增加图片下载超时时间"
            )
            self.issues.append(issue)
    
    def _analyze_errors(self, page_details: List[Dict[str, Any]], total_retries: int, total_errors: int):
        """分析错误和重试"""
        issue = Issue(
            severity="medium",
            category="错误和重试",
            description=f"总重试次数: {total_retries}, 总错误次数: {total_errors}",
            affected_pages=[p['name'] for p in page_details if p.get('retry_count', 0) > 0 or p.get('error_message')],
            suggested_solution="分析错误日志，识别常见错误模式，针对性地优化错误处理逻辑"
        )
        self.issues.append(issue)
    
    def _generate_recommendations(self, summary: Dict[str, Any]):
        """生成改进建议"""
        # 基于成功率生成建议
        success_rate = summary["crawl_summary"]["success_rate_percent"]
        if success_rate < 100:
            self.recommendations.append(Recommendation(
                priority="high",
                category="稳定性",
                description="增加重试次数和超时时间，提高爬取稳定性",
                rationale=f"当前成功率为 {success_rate}%，需要提高稳定性以确保所有页面都能成功爬取"
            ))
        
        # 基于性能生成建议
        avg_load_time = summary["performance_metrics"]["average_load_time_seconds"]
        if avg_load_time > 10:
            self.recommendations.append(Recommendation(
                priority="medium",
                category="性能",
                description="优化页面加载策略，减少等待时间",
                rationale=f"平均加载时间 {avg_load_time:.2f} 秒，可以通过优化等待条件提高效率"
            ))
        
        # 基于内容提取生成建议
        avg_content_length = summary["performance_metrics"]["average_content_length"]
        if avg_content_length < 500:
            self.recommendations.append(Recommendation(
                priority="high",
                category="数据质量",
                description="审查和优化页面解析规则，确保内容完整提取",
                rationale=f"平均内容长度 {avg_content_length:.0f} 字符，可能存在内容提取不完整的问题"
            ))
        
        # 基于资源下载生成建议
        total_images = summary["resource_metrics"]["total_images_downloaded"]
        if total_images > 0:
            self.recommendations.append(Recommendation(
                priority="medium",
                category="资源管理",
                description="实现图片下载进度监控和失败重试机制",
                rationale=f"已下载 {total_images} 张图片，需要确保所有图片都能成功下载"
            ))
        
        # 通用建议
        self.recommendations.append(Recommendation(
            priority="medium",
            category="监控",
            description="实施实时监控和告警机制，及时发现和处理问题",
            rationale="实时监控可以帮助快速识别和解决问题，提高爬取效率"
        ))
        
        self.recommendations.append(Recommendation(
            priority="low",
            category="文档",
            description="完善爬取流程文档和操作手册",
            rationale="良好的文档可以帮助团队成员快速理解和维护爬取系统"
        ))
    
    def generate_report(self, filename: Optional[str] = None) -> str:
        """生成试行爬取报告
        
        Args:
            filename: 报告文件名（可选）
            
        Returns:
            报告文件路径
        """
        # 分析结果
        self.analyze_results()
        
        # 生成文件名
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trial_crawl_report_{timestamp}.md"
        
        filepath = self.output_dir / filename
        
        # 生成报告内容
        report_content = self._generate_report_content()
        
        # 保存报告
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"试行爬取报告已生成: {filepath}")
        
        return str(filepath)
    
    def _generate_report_content(self) -> str:
        """生成报告内容
        
        Returns:
            报告内容字符串
        """
        summary = self.monitor.get_summary()
        page_details = self.monitor.get_page_details()
        
        content = []
        
        # 标题
        content.append("# 页面爬取试行方案报告\n")
        content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        content.append(f"**报告版本**: 1.0\n\n")
        
        # 执行摘要
        content.append("## 执行摘要\n\n")
        content.append("本报告记录了页面爬取试行方案的执行情况，包括爬取结果统计、遇到的问题及解决方案建议。\n\n")
        
        # 爬取配置
        content.append("## 爬取配置\n\n")
        content.append("### 基本参数\n\n")
        content.append(f"- **请求延迟**: {self.config.request_delay_min}-{self.config.request_delay_max} 秒\n")
        content.append(f"- **最大重试次数**: {self.config.max_retries}\n")
        content.append(f"- **超时时间**: {self.config.timeout} 秒\n")
        content.append(f"- **页面加载等待策略**: {self.config.wait_until}\n")
        content.append(f"- **额外等待时间**: {self.config.additional_wait} 毫秒\n\n")
        
        content.append("### 数据提取配置\n\n")
        content.append(f"- **提取标题**: {'是' if self.config.extract_title else '否'}\n")
        content.append(f"- **提取内容**: {'是' if self.config.extract_content else '否'}\n")
        content.append(f"- **提取链接**: {'是' if self.config.extract_links else '否'}\n")
        content.append(f"- **提取图片**: {'是' if self.config.extract_images else '否'}\n")
        content.append(f"- **最小内容长度**: {self.config.min_content_length} 字符\n\n")
        
        # 爬取结果统计
        content.append("## 爬取结果统计\n\n")
        
        crawl_summary = summary["crawl_summary"]
        content.append("### 总体统计\n\n")
        content.append(f"- **开始时间**: {crawl_summary['start_time']}\n")
        content.append(f"- **结束时间**: {crawl_summary['end_time']}\n")
        content.append(f"- **总耗时**: {crawl_summary['duration_seconds']:.2f} 秒\n")
        content.append(f"- **总页面数**: {crawl_summary['total_pages']}\n")
        content.append(f"- **成功页面**: {crawl_summary['successful_pages']}\n")
        content.append(f"- **失败页面**: {crawl_summary['failed_pages']}\n")
        content.append(f"- **成功率**: {crawl_summary['success_rate_percent']}%\n")
        content.append(f"- **总重试次数**: {crawl_summary['total_retries']}\n")
        content.append(f"- **总错误次数**: {crawl_summary['total_errors']}\n\n")
        
        perf_metrics = summary["performance_metrics"]
        content.append("### 性能指标\n\n")
        content.append(f"- **总加载时间**: {perf_metrics['total_load_time_seconds']} 秒\n")
        content.append(f"- **平均加载时间**: {perf_metrics['average_load_time_seconds']} 秒\n")
        content.append(f"- **总内容长度**: {perf_metrics['total_content_length']} 字符\n")
        content.append(f"- **平均内容长度**: {perf_metrics['average_content_length']} 字符\n\n")
        
        res_metrics = summary["resource_metrics"]
        content.append("### 资源指标\n\n")
        content.append(f"- **下载图片总数**: {res_metrics['total_images_downloaded']}\n")
        content.append(f"- **提取链接总数**: {res_metrics['total_links_extracted']}\n")
        content.append(f"- **平均每页图片**: {res_metrics['average_images_per_page']}\n")
        content.append(f"- **平均每页链接**: {res_metrics['average_links_per_page']}\n\n")
        
        # 页面详情
        content.append("## 页面详情\n\n")
        content.append("| 页面名称 | URL | 状态 | 加载时间(秒) | 内容长度 | 图片数 | 链接数 | 重试次数 |\n")
        content.append("|---------|-----|------|-------------|----------|--------|--------|----------|\n")
        
        for page in page_details:
            status = "✓" if page.get('is_success', False) else "✗"
            load_time = page.get('load_time', 0)
            content_length = page.get('content_length', 0)
            image_count = page.get('image_count', 0)
            link_count = page.get('link_count', 0)
            retry_count = page.get('retry_count', 0)
            
            content.append(f"| {page['name']} | {page['url'][:50]}... | {status} | {load_time:.2f} | {content_length} | {image_count} | {link_count} | {retry_count} |\n")
        
        content.append("\n")
        
        # 问题分析
        content.append("## 问题分析\n\n")
        
        if self.issues:
            for i, issue in enumerate(self.issues, 1):
                content.append(f"### 问题 {i}: {issue.category} ({issue.severity.upper()})\n\n")
                content.append(f"**描述**: {issue.description}\n\n")
                content.append(f"**受影响页面**: {', '.join(issue.affected_pages)}\n\n")
                content.append(f"**建议解决方案**: {issue.suggested_solution}\n\n")
        else:
            content.append("未发现明显问题。\n\n")
        
        # 解决方案建议
        content.append("## 解决方案建议\n\n")
        
        if self.recommendations:
            for i, rec in enumerate(self.recommendations, 1):
                content.append(f"### 建议 {i}: {rec.category} ({rec.priority.upper()})\n\n")
                content.append(f"**描述**: {rec.description}\n\n")
                content.append(f"**理由**: {rec.rationale}\n\n")
        else:
            content.append("暂无额外建议。\n\n")
        
        # 可行性评估
        content.append("## 可行性评估\n\n")
        
        success_rate = crawl_summary['success_rate_percent']
        if success_rate >= 90:
            feasibility = "高"
            assessment = "爬取逻辑基本可行，可以进行小规模批量爬取测试。"
        elif success_rate >= 70:
            feasibility = "中"
            assessment = "爬取逻辑基本可行，但需要解决部分问题后才能进行批量爬取。"
        else:
            feasibility = "低"
            assessment = "爬取逻辑存在较多问题，需要重点优化后再进行批量爬取。"
        
        content.append(f"**可行性评级**: {feasibility}\n\n")
        content.append(f"**评估结论**: {assessment}\n\n")
        
        # 下一步计划
        content.append("## 下一步计划\n\n")
        content.append("1. 根据本报告中的问题分析和建议，优化爬取逻辑\n")
        content.append("2. 针对失败页面进行单独测试和调试\n")
        content.append("3. 调整爬取参数，提高成功率和性能\n")
        content.append("4. 进行更大规模的批量爬取测试\n")
        content.append("5. 完善监控和告警机制\n\n")
        
        # 附录
        content.append("## 附录\n\n")
        content.append("### 配置文件\n\n")
        content.append("- 试行爬取配置: `trial_crawl_config.py`\n")
        content.append("- 监控器: `trial_crawl_monitor.py`\n")
        content.append("- 爬取器: `trial_crawler.py`\n")
        content.append("- 报告生成器: `trial_crawl_report.py`\n\n")
        
        content.append("### 日志文件\n\n")
        content.append(f"- 爬取日志: `{self.config.log_dir}/trial_crawl_*.log`\n")
        content.append(f"- 指标数据: `{self.config.log_dir}/trial_metrics_*.json`\n\n")
        
        content.append("---\n\n")
        content.append("*报告生成完毕*")
        
        return "\n".join(content)
