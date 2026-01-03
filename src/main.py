#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
原神千星奇域·综合指南 - 网站爬取主程序
"""

import os
import sys
import json
import logging
from crawler.spider import Spider
from crawler.parser import Parser
from crawler.downloader import Downloader

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入配置模块的日志
from config import logger

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
# URL列表文件路径
URL_LIST_FILE = os.path.join(DATA_DIR, "url_list.txt")
# 文档ID映射表文件路径
DOC_ID_MAP_FILE = os.path.join(DATA_DIR, "doc_id_map.json")
# Markdown保存目录
MARKDOWN_DIR = os.path.join(DATA_DIR, "markdown")
# 图片保存目录
IMAGES_DIR = os.path.join(DATA_DIR, "images")


def load_doc_id_map():
    """加载文档ID映射表"""
    try:
        with open(DOC_ID_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load doc_id_map: {e}")
        return {}


def load_url_list():
    """加载待爬取URL列表"""
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


def crawl_single_page(url, spider, parser, downloader, doc_id_map):
    """爬取单个页面
    
    Args:
        url: 页面URL
        spider: Spider对象
        parser: Parser对象
        downloader: Downloader对象
        doc_id_map: 文档ID映射表
        
    Returns:
        dict: 爬取结果
    """
    result = {
        "url": url,
        "success": False,
        "title": None,
        "content_length": 0,
        "links_found": 0,
        "images_found": 0,
        "images_downloaded": 0,
        "error": None
    }
    
    try:
        # 获取页面内容
        logger.info(f"Crawling page: {url}")
        page_content = spider.get_page(url)
        
        if not page_content:
            result["error"] = "Failed to get page content"
            return result
        
        # 解析页面内容
        parsed_content = parser.parse_content(page_content)
        if not parsed_content:
            result["error"] = "Failed to parse content"
            return result
        
        # 提取文档ID和标题
        doc_id = url.split('/')[-1]
        title = doc_id_map.get(doc_id, doc_id)
        result["title"] = title
        result["content_length"] = len(parsed_content['content'])
        
        # 解析页面中的链接
        links = parser.parse_links(page_content, url)
        result["links_found"] = len(links)
        
        # 解析页面中的图片
        images = parser.parse_images(page_content)
        result["images_found"] = len(images)
        
        # 保存Markdown文件
        filename = downloader.save_markdown(parsed_content['content'], title, MARKDOWN_DIR)
        if not filename:
            result["error"] = "Failed to save Markdown"
            return result
        
        logger.info(f"Saved Markdown file: {filename}")
        
        # 下载图片
        images_downloaded = 0
        for img_url in images:
            downloaded_filename = downloader.download_image(img_url, IMAGES_DIR)
            if downloaded_filename:
                images_downloaded += 1
                logger.info(f"Downloaded image: {downloaded_filename}")
            else:
                logger.warning(f"Failed to download image: {img_url}")
        
        result["images_downloaded"] = images_downloaded
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Error crawling {url}: {e}", exc_info=True)
    
    return result


def crawl_batch(url_list, spider, parser, downloader, doc_id_map, max_concurrent=5, retry_times=3):
    """批量爬取页面
    
    Args:
        url_list: 待爬取URL列表
        spider: Spider对象
        parser: Parser对象
        downloader: Downloader对象
        doc_id_map: 文档ID映射表
        max_concurrent: 最大并发数
        retry_times: 重试次数
        
    Returns:
        dict: 爬取统计结果
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    # 初始化统计数据
    stats = {
        "total_urls": len(url_list),
        "success": 0,
        "failed": 0,
        "retry_count": 0,
        "total_content_length": 0,
        "total_links_found": 0,
        "total_images_found": 0,
        "total_images_downloaded": 0,
        "failed_urls": []
    }
    
    logger.info(f"开始批量爬取，共 {len(url_list)} 个URL，最大并发数: {max_concurrent}")
    
    # 使用线程池进行并发爬取
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # 提交所有爬取任务
        future_to_url = {executor.submit(crawl_single_page, url, spider, parser, downloader, doc_id_map): url for url in url_list}
        
        # 处理爬取结果
        for i, future in enumerate(as_completed(future_to_url), 1):
            url = future_to_url[future]
            
            try:
                result = future.result()
                
                if result["success"]:
                    stats["success"] += 1
                    stats["total_content_length"] += result["content_length"]
                    stats["total_links_found"] += result["links_found"]
                    stats["total_images_found"] += result["images_found"]
                    stats["total_images_downloaded"] += result["images_downloaded"]
                    logger.info(f"[{i}/{len(url_list)}] 爬取成功: {result['title']} ({result['content_length']} 字符)")
                else:
                    stats["failed"] += 1
                    stats["failed_urls"].append({
                        "url": url,
                        "error": result["error"]
                    })
                    logger.error(f"[{i}/{len(url_list)}] 爬取失败: {url} - {result['error']}")
                    
                    # 重试逻辑
                    if retry_times > 0:
                        for retry in range(1, retry_times + 1):
                            logger.info(f"[{i}/{len(url_list)}] 重试 {retry}/{retry_times}: {url}")
                            retry_result = crawl_single_page(url, spider, parser, downloader, doc_id_map)
                            stats["retry_count"] += 1
                            
                            if retry_result["success"]:
                                stats["success"] += 1
                                stats["failed"] -= 1
                                stats["failed_urls"].pop()
                                stats["total_content_length"] += retry_result["content_length"]
                                stats["total_links_found"] += retry_result["links_found"]
                                stats["total_images_found"] += retry_result["images_found"]
                                stats["total_images_downloaded"] += retry_result["images_downloaded"]
                                logger.info(f"[{i}/{len(url_list)}] 重试成功: {retry_result['title']}")
                                break
                            else:
                                logger.error(f"[{i}/{len(url_list)}] 重试 {retry}/{retry_times} 失败: {url} - {retry_result['error']}")
                
            except Exception as e:
                stats["failed"] += 1
                stats["failed_urls"].append({
                    "url": url,
                    "error": str(e)
                })
                logger.error(f"[{i}/{len(url_list)}] 处理结果时出错: {url} - {e}", exc_info=True)
    
    return stats


def generate_progress_report(stats):
    """生成进度报告
    
    Args:
        stats: 爬取统计结果
        
    Returns:
        str: 进度报告内容
    """
    from datetime import datetime
    
    report = f"# 爬取进度报告\n\n"
    report += f"## 基本信息\n"
    report += f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"- 总URL数: {stats['total_urls']}\n"
    report += f"- 成功数: {stats['success']}\n"
    report += f"- 失败数: {stats['failed']}\n"
    report += f"- 重试次数: {stats['retry_count']}\n"
    report += f"- 成功率: {stats['success'] / stats['total_urls'] * 100:.2f}%\n\n"
    
    report += f"## 内容统计\n"
    report += f"- 总内容长度: {stats['total_content_length']} 字符\n"
    report += f"- 平均内容长度: {stats['total_content_length'] / stats['success'] if stats['success'] > 0 else 0:.0f} 字符/文档\n"
    report += f"- 总链接数: {stats['total_links_found']}\n"
    report += f"- 总图片数: {stats['total_images_found']}\n"
    report += f"- 成功下载图片数: {stats['total_images_downloaded']}\n"
    report += f"- 图片下载率: {stats['total_images_downloaded'] / stats['total_images_found'] * 100:.2f}%\n\n"
    
    if stats['failed_urls']:
        report += f"## 失败URL列表\n"
        for failed in stats['failed_urls']:
            report += f"- {failed['url']}: {failed['error']}\n"
    
    return report


def main():
    """主程序入口"""
    logger.info("Starting crawl process...")
    
    # 确保保存目录存在
    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    try:
        # 加载配置数据
        logger.info("Loading configuration data...")
        doc_id_map = load_doc_id_map()
        url_list = load_url_list()
        
        if not url_list:
            logger.error("No URLs to crawl. Please run initial_data_collection.py first.")
            return
        
        logger.info(f"Loaded {len(url_list)} URLs to crawl")
        logger.info(f"Loaded {len(doc_id_map)} document mappings")
        
        # 初始化爬虫组件
        spider = Spider()
        parser = Parser()
        downloader = Downloader()
        
        # 测试单页面爬取
        logger.info("Testing single page crawl...")
        test_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
        crawl_result = crawl_single_page(test_url, spider, parser, downloader, doc_id_map)
        
        if crawl_result["success"]:
            logger.info(f"Single page crawl test successful: {crawl_result['title']}")
            logger.info(f"  Content length: {crawl_result['content_length']} characters")
            logger.info(f"  Links found: {crawl_result['links_found']}")
            logger.info(f"  Images found: {crawl_result['images_found']}")
            logger.info(f"  Images downloaded: {crawl_result['images_downloaded']}")
        else:
            logger.error(f"Single page crawl test failed: {crawl_result['error']}")
            return
        
        # 批量爬取逻辑
        logger.info("开始批量爬取...")
        
        # 爬取前50个文档（Phase 3-T1）
        logger.info("===== 开始爬取第1-50个文档 =====")
        batch_stats_1 = crawl_batch(url_list[:50], spider, parser, downloader, doc_id_map, max_concurrent=3)
        
        # 生成进度报告
        report_1 = generate_progress_report(batch_stats_1)
        report_path_1 = os.path.join(DATA_DIR, "crawl_report_phase1.md")
        with open(report_path_1, 'w', encoding='utf-8') as f:
            f.write(report_1)
        logger.info(f"Phase 1 爬取报告已保存到: {report_path_1}")
        
        # 爬取第51-100个文档（Phase 3-T2）
        logger.info("===== 开始爬取第51-100个文档 =====")
        batch_stats_2 = crawl_batch(url_list[50:100], spider, parser, downloader, doc_id_map, max_concurrent=3)
        
        # 生成进度报告
        report_2 = generate_progress_report(batch_stats_2)
        report_path_2 = os.path.join(DATA_DIR, "crawl_report_phase2.md")
        with open(report_path_2, 'w', encoding='utf-8') as f:
            f.write(report_2)
        logger.info(f"Phase 2 爬取报告已保存到: {report_path_2}")
        
        # 爬取剩余文档（Phase 3-T3）
        logger.info("===== 开始爬取第101-167个文档 =====")
        batch_stats_3 = crawl_batch(url_list[100:], spider, parser, downloader, doc_id_map, max_concurrent=3)
        
        # 生成进度报告
        report_3 = generate_progress_report(batch_stats_3)
        report_path_3 = os.path.join(DATA_DIR, "crawl_report_phase3.md")
        with open(report_path_3, 'w', encoding='utf-8') as f:
            f.write(report_3)
        logger.info(f"Phase 3 爬取报告已保存到: {report_path_3}")
        
        # 生成总报告
        total_stats = {
            "total_urls": batch_stats_1["total_urls"] + batch_stats_2["total_urls"] + batch_stats_3["total_urls"],
            "success": batch_stats_1["success"] + batch_stats_2["success"] + batch_stats_3["success"],
            "failed": batch_stats_1["failed"] + batch_stats_2["failed"] + batch_stats_3["failed"],
            "retry_count": batch_stats_1["retry_count"] + batch_stats_2["retry_count"] + batch_stats_3["retry_count"],
            "total_content_length": batch_stats_1["total_content_length"] + batch_stats_2["total_content_length"] + batch_stats_3["total_content_length"],
            "total_links_found": batch_stats_1["total_links_found"] + batch_stats_2["total_links_found"] + batch_stats_3["total_links_found"],
            "total_images_found": batch_stats_1["total_images_found"] + batch_stats_2["total_images_found"] + batch_stats_3["total_images_found"],
            "total_images_downloaded": batch_stats_1["total_images_downloaded"] + batch_stats_2["total_images_downloaded"] + batch_stats_3["total_images_downloaded"],
            "failed_urls": batch_stats_1["failed_urls"] + batch_stats_2["failed_urls"] + batch_stats_3["failed_urls"]
        }
        
        total_report = generate_progress_report(total_stats)
        total_report_path = os.path.join(DATA_DIR, "crawl_report_total.md")
        with open(total_report_path, 'w', encoding='utf-8') as f:
            f.write(total_report)
        logger.info(f"总爬取报告已保存到: {total_report_path}")
        
        # 打印最终统计结果
        logger.info("===== 最终爬取统计 =====")
        logger.info(f"总URL数: {total_stats['total_urls']}")
        logger.info(f"成功数: {total_stats['success']}")
        logger.info(f"失败数: {total_stats['failed']}")
        logger.info(f"成功率: {total_stats['success'] / total_stats['total_urls'] * 100:.2f}%")
        logger.info(f"总内容长度: {total_stats['total_content_length']} 字符")
        logger.info(f"总图片数: {total_stats['total_images_found']}")
        logger.info(f"成功下载图片数: {total_stats['total_images_downloaded']}")
        
    except Exception as e:
        logger.error(f"An error occurred during crawl: {e}", exc_info=True)
    
    logger.info("Crawl process completed.")


if __name__ == "__main__":
    main()
