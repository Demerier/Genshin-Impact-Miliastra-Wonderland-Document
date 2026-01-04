#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
试行爬取主程序入口
用于执行页面爬取试行方案，生成详细的试行报告
"""

import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from trial_crawler import TrialCrawler
from trial_crawl_config import TRIAL_CONFIG, TRIAL_PAGES


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='页面爬取试行方案 - 测试爬取逻辑的可行性和有效性'
    )
    
    parser.add_argument(
        '--pages',
        type=int,
        default=len(TRIAL_PAGES),
        help=f'要爬取的页面数量 (默认: {len(TRIAL_PAGES)})'
    )
    
    parser.add_argument(
        '--delay-min',
        type=float,
        default=TRIAL_CONFIG.request_delay_min,
        help=f'最小请求延迟秒数 (默认: {TRIAL_CONFIG.request_delay_min})'
    )
    
    parser.add_argument(
        '--delay-max',
        type=float,
        default=TRIAL_CONFIG.request_delay_max,
        help=f'最大请求延迟秒数 (默认: {TRIAL_CONFIG.request_delay_max})'
    )
    
    parser.add_argument(
        '--max-retries',
        type=int,
        default=TRIAL_CONFIG.max_retries,
        help=f'最大重试次数 (默认: {TRIAL_CONFIG.max_retries})'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=TRIAL_CONFIG.timeout,
        help=f'请求超时时间秒数 (默认: {TRIAL_CONFIG.timeout})'
    )
    
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='不生成详细报告'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    args = parser.parse_args()
    
    # 更新配置
    config = TRIAL_CONFIG
    config.request_delay_min = args.delay_min
    config.request_delay_max = args.delay_max
    config.max_retries = args.max_retries
    config.timeout = args.timeout
    
    if args.verbose:
        config.log_level = "DEBUG"
    
    # 选择要爬取的页面
    pages_to_crawl = TRIAL_PAGES[:args.pages]
    
    print("=" * 80)
    print("页面爬取试行方案")
    print("=" * 80)
    print(f"\n配置信息:")
    print(f"  - 爬取页面数: {len(pages_to_crawl)}")
    print(f"  - 请求延迟: {config.request_delay_min}-{config.request_delay_max} 秒")
    print(f"  - 最大重试: {config.max_retries} 次")
    print(f"  - 超时时间: {config.timeout} 秒")
    print(f"  - 日志级别: {config.log_level}")
    print(f"\n目标页面:")
    for i, page in enumerate(pages_to_crawl, 1):
        print(f"  {i}. {page.name}: {page.url}")
    print("\n" + "=" * 80 + "\n")
    
    # 创建爬取器
    crawler = TrialCrawler(config=config)
    
    try:
        # 运行试行爬取
        print("开始试行爬取...\n")
        summary = crawler.run_trial(pages=pages_to_crawl)
        
        # 生成报告
        if not args.no_report:
            print("\n生成试行爬取报告...")
            report_file = crawler.generate_report()
            print(f"\n报告已生成: {report_file}")
        
        # 打印最终摘要
        print("\n" + "=" * 80)
        print("试行爬取完成")
        print("=" * 80)
        
        crawl_summary = summary["crawl_summary"]
        print(f"\n最终统计:")
        print(f"  - 总页面数: {crawl_summary['total_pages']}")
        print(f"  - 成功页面: {crawl_summary['successful_pages']}")
        print(f"  - 失败页面: {crawl_summary['failed_pages']}")
        print(f"  - 成功率: {crawl_summary['success_rate_percent']}%")
        print(f"  - 总耗时: {crawl_summary['duration_seconds']:.2f} 秒")
        
        # 返回退出码
        if crawl_summary['success_rate_percent'] >= 80:
            print("\n✓ 试行爬取成功！爬取逻辑可行。")
            return 0
        else:
            print("\n✗ 试行爬取存在问题，请查看报告了解详情。")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n用户中断爬取")
        return 130
    except Exception as e:
        print(f"\n\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
