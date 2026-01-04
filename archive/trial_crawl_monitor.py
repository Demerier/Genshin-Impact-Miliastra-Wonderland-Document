#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
试行爬取监控器
负责记录爬取过程中的各项指标，包括响应状态码、页面加载时间、数据提取成功率等
"""

import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class PageMetrics:
    """单个页面的爬取指标"""
    
    url: str
    name: str
    
    # 基础指标
    status_code: Optional[int] = None
    load_time: float = 0.0
    retry_count: int = 0
    
    # 内容指标
    content_length: int = 0
    title_extracted: bool = False
    content_extracted: bool = False
    links_extracted: bool = False
    images_extracted: bool = False
    
    # 资源指标
    image_count: int = 0
    images_downloaded: int = 0
    link_count: int = 0
    
    # 错误信息
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    
    # 时间戳
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        self.start_time = datetime.now().isoformat()
    
    def mark_success(self, status_code: int, load_time: float):
        """标记爬取成功"""
        self.status_code = status_code
        self.load_time = load_time
        self.end_time = datetime.now().isoformat()
    
    def mark_failure(self, error_message: str, error_type: str = "Exception"):
        """标记爬取失败"""
        self.error_message = error_message
        self.error_type = error_type
        self.end_time = datetime.now().isoformat()
    
    def add_retry(self):
        """增加重试次数"""
        self.retry_count += 1
    
    def update_content_metrics(self, title: bool, content: bool, links: bool, images: bool, length: int):
        """更新内容提取指标"""
        self.title_extracted = title
        self.content_extracted = content
        self.links_extracted = links
        self.images_extracted = images
        self.content_length = length
    
    def update_resource_metrics(self, image_count: int, images_downloaded: int, link_count: int):
        """更新资源指标"""
        self.image_count = image_count
        self.images_downloaded = images_downloaded
        self.link_count = link_count
    
    def is_success(self) -> bool:
        """判断是否成功"""
        return self.status_code is not None and self.status_code == 200 and self.error_message is None
    
    def get_extraction_success_rate(self) -> float:
        """计算数据提取成功率"""
        total_fields = 4
        extracted_fields = sum([
            self.title_extracted,
            self.content_extracted,
            self.links_extracted,
            self.images_extracted
        ])
        return (extracted_fields / total_fields) * 100 if total_fields > 0 else 0.0


class CrawlMonitor:
    """爬取监控器"""
    
    def __init__(self, output_dir: str = "logs/trial"):
        """初始化监控器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.page_metrics: List[PageMetrics] = []
        self.current_metrics: Optional[PageMetrics] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        # 统计数据
        self.total_pages = 0
        self.successful_pages = 0
        self.failed_pages = 0
        self.total_retries = 0
        self.total_errors = 0
        self.total_load_time = 0.0
        self.total_content_length = 0
        self.total_images_downloaded = 0
        self.total_links_extracted = 0
    
    def start_crawl(self):
        """开始爬取监控"""
        self.start_time = datetime.now()
        print(f"[监控] 爬取开始于: {self.start_time.isoformat()}")
    
    def end_crawl(self):
        """结束爬取监控"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"[监控] 爬取结束于: {self.end_time.isoformat()}")
        print(f"[监控] 总耗时: {duration:.2f}秒")
    
    def start_page(self, url: str, name: str) -> PageMetrics:
        """开始监控单个页面
        
        Args:
            url: 页面URL
            name: 页面名称
            
        Returns:
            页面指标对象
        """
        self.current_metrics = PageMetrics(url=url, name=name)
        self.total_pages += 1
        print(f"[监控] 开始爬取页面: {name} ({url})")
        return self.current_metrics
    
    def end_page(self, success: bool, status_code: Optional[int] = None, load_time: float = 0.0):
        """结束监控单个页面
        
        Args:
            success: 是否成功
            status_code: HTTP状态码
            load_time: 加载时间
        """
        if self.current_metrics:
            if success:
                self.current_metrics.mark_success(status_code, load_time)
                self.successful_pages += 1
                self.total_load_time += load_time
                print(f"[监控] 页面爬取成功: {self.current_metrics.name} (状态码: {status_code}, 加载时间: {load_time:.2f}秒)")
            else:
                self.failed_pages += 1
                self.total_errors += 1
                print(f"[监控] 页面爬取失败: {self.current_metrics.name} (错误: {self.current_metrics.error_message})")
            
            self.page_metrics.append(self.current_metrics)
            self.current_metrics = None
    
    def record_retry(self):
        """记录重试"""
        if self.current_metrics:
            self.current_metrics.add_retry()
            self.total_retries += 1
            print(f"[监控] 页面重试: {self.current_metrics.name} (重试次数: {self.current_metrics.retry_count})")
    
    def record_error(self, error_message: str, error_type: str = "Exception"):
        """记录错误"""
        if self.current_metrics:
            self.current_metrics.mark_failure(error_message, error_type)
            print(f"[监控] 页面错误: {self.current_metrics.name} ({error_type}: {error_message})")
    
    def update_page_content_metrics(self, title: bool, content: bool, links: bool, images: bool, length: int):
        """更新页面内容指标"""
        if self.current_metrics:
            self.current_metrics.update_content_metrics(title, content, links, images, length)
            self.total_content_length += length
            print(f"[监控] 内容指标更新 - 标题: {title}, 内容: {content}, 链接: {links}, 图片: {images}, 长度: {length}")
    
    def update_page_resource_metrics(self, image_count: int, images_downloaded: int, link_count: int):
        """更新页面资源指标"""
        if self.current_metrics:
            self.current_metrics.update_resource_metrics(image_count, images_downloaded, link_count)
            self.total_images_downloaded += images_downloaded
            self.total_links_extracted += link_count
            print(f"[监控] 资源指标更新 - 图片数: {image_count}, 下载: {images_downloaded}, 链接数: {link_count}")
    
    def get_summary(self) -> Dict[str, Any]:
        """获取爬取摘要
        
        Returns:
            摘要字典
        """
        duration = 0.0
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        avg_load_time = self.total_load_time / self.successful_pages if self.successful_pages > 0 else 0.0
        avg_content_length = self.total_content_length / self.successful_pages if self.successful_pages > 0 else 0.0
        success_rate = (self.successful_pages / self.total_pages * 100) if self.total_pages > 0 else 0.0
        
        summary = {
            "crawl_summary": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration_seconds": duration,
                "total_pages": self.total_pages,
                "successful_pages": self.successful_pages,
                "failed_pages": self.failed_pages,
                "success_rate_percent": round(success_rate, 2),
                "total_retries": self.total_retries,
                "total_errors": self.total_errors
            },
            "performance_metrics": {
                "total_load_time_seconds": round(self.total_load_time, 2),
                "average_load_time_seconds": round(avg_load_time, 2),
                "total_content_length": self.total_content_length,
                "average_content_length": round(avg_content_length, 2)
            },
            "resource_metrics": {
                "total_images_downloaded": self.total_images_downloaded,
                "total_links_extracted": self.total_links_extracted,
                "average_images_per_page": round(self.total_images_downloaded / self.successful_pages, 2) if self.successful_pages > 0 else 0.0,
                "average_links_per_page": round(self.total_links_extracted / self.successful_pages, 2) if self.successful_pages > 0 else 0.0
            }
        }
        
        return summary
    
    def get_page_details(self) -> List[Dict[str, Any]]:
        """获取所有页面的详细指标
        
        Returns:
            页面指标列表
        """
        return [asdict(metric) for metric in self.page_metrics]
    
    def save_metrics(self, filename: Optional[str] = None) -> str:
        """保存指标到JSON文件
        
        Args:
            filename: 文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"trial_metrics_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        metrics_data = {
            "summary": self.get_summary(),
            "page_details": self.get_page_details()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)
        
        print(f"[监控] 指标已保存到: {filepath}")
        return str(filepath)
    
    def print_summary(self):
        """打印爬取摘要"""
        summary = self.get_summary()
        
        print("\n" + "=" * 80)
        print("试行爬取摘要报告")
        print("=" * 80)
        
        print("\n【爬取统计】")
        crawl_summary = summary["crawl_summary"]
        print(f"  开始时间: {crawl_summary['start_time']}")
        print(f"  结束时间: {crawl_summary['end_time']}")
        print(f"  总耗时: {crawl_summary['duration_seconds']:.2f}秒")
        print(f"  总页面数: {crawl_summary['total_pages']}")
        print(f"  成功页面: {crawl_summary['successful_pages']}")
        print(f"  失败页面: {crawl_summary['failed_pages']}")
        print(f"  成功率: {crawl_summary['success_rate_percent']}%")
        print(f"  总重试次数: {crawl_summary['total_retries']}")
        print(f"  总错误次数: {crawl_summary['total_errors']}")
        
        print("\n【性能指标】")
        perf_metrics = summary["performance_metrics"]
        print(f"  总加载时间: {perf_metrics['total_load_time_seconds']}秒")
        print(f"  平均加载时间: {perf_metrics['average_load_time_seconds']}秒")
        print(f"  总内容长度: {perf_metrics['total_content_length']}字符")
        print(f"  平均内容长度: {perf_metrics['average_content_length']}字符")
        
        print("\n【资源指标】")
        res_metrics = summary["resource_metrics"]
        print(f"  下载图片总数: {res_metrics['total_images_downloaded']}")
        print(f"  提取链接总数: {res_metrics['total_links_extracted']}")
        print(f"  平均每页图片: {res_metrics['average_images_per_page']}")
        print(f"  平均每页链接: {res_metrics['average_links_per_page']}")
        
        print("\n" + "=" * 80)
