import logging
from typing import Dict, List, Optional
from playwright.sync_api import Page, Browser, BrowserContext
from dataclasses import dataclass
from datetime import datetime
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class LoadDetectionResult:
    """页面加载检测结果"""
    url: str
    success: bool
    load_time: float
    detection_steps: List[str]
    errors: List[str]
    metrics: Dict[str, float]


class PageLoadDetector:
    """页面加载检测器 - 多维度检测"""

    def __init__(self, timeout: int = 30000):
        """
        初始化检测器
        
        Args:
            timeout: 超时时间（毫秒）
        """
        self.timeout = timeout
        self.detection_steps = []
        self.errors = []

    def wait_for_network_idle(self, page: Page) -> bool:
        """
        等待网络空闲
        
        Args:
            page: Playwright页面对象
            
        Returns:
            是否成功
        """
        try:
            self.detection_steps.append("等待网络空闲")
            start_time = time.time()
            page.wait_for_load_state('networkidle', timeout=self.timeout)
            elapsed = time.time() - start_time
            logger.info(f"网络空闲检测完成，耗时: {elapsed:.2f}秒")
            return True
        except Exception as e:
            error_msg = f"网络空闲检测失败: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def wait_for_dom_ready(self, page: Page) -> bool:
        """
        等待DOM准备就绪
        
        Args:
            page: Playwright页面对象
            
        Returns:
            是否成功
        """
        try:
            self.detection_steps.append("等待DOM准备就绪")
            start_time = time.time()
            page.wait_for_load_state('domcontentloaded', timeout=self.timeout)
            elapsed = time.time() - start_time
            logger.info(f"DOM准备就绪，耗时: {elapsed:.2f}秒")
            return True
        except Exception as e:
            error_msg = f"DOM准备就绪检测失败: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def check_element_visibility(self, page: Page, selectors: List[str]) -> bool:
        """
        检查关键元素可见性
        
        Args:
            page: Playwright页面对象
            selectors: CSS选择器列表
            
        Returns:
            是否所有元素都可见
        """
        try:
            self.detection_steps.append(f"检查{len(selectors)}个关键元素可见性")
            start_time = time.time()
            
            visible_count = 0
            for selector in selectors:
                try:
                    element = page.wait_for_selector(
                        selector,
                        state='visible',
                        timeout=5000
                    )
                    if element:
                        visible_count += 1
                        logger.info(f"元素可见: {selector}")
                except:
                    logger.warning(f"元素不可见: {selector}")
            
            elapsed = time.time() - start_time
            logger.info(f"元素可见性检测完成: {visible_count}/{len(selectors)}，耗时: {elapsed:.2f}秒")
            return visible_count > 0
        except Exception as e:
            error_msg = f"元素可见性检测失败: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def check_image_loading(self, page: Page) -> Dict[str, int]:
        """
        检查图片加载状态
        
        Args:
            page: Playwright页面对象
            
        Returns:
            图片加载统计信息
        """
        try:
            self.detection_steps.append("检查图片加载状态")
            start_time = time.time()
            
            stats = {
                'total': 0,
                'loaded': 0,
                'failed': 0,
                'loading': 0
            }
            
            images = page.query_selector_all('img')
            stats['total'] = len(images)
            
            for img in images:
                try:
                    natural_width = img.evaluate('el => el.naturalWidth')
                    if natural_width > 0:
                        stats['loaded'] += 1
                    else:
                        stats['failed'] += 1
                except:
                    stats['failed'] += 1
            
            elapsed = time.time() - start_time
            logger.info(f"图片加载检测完成: {stats['loaded']}/{stats['total']}，耗时: {elapsed:.2f}秒")
            return stats
        except Exception as e:
            error_msg = f"图片加载检测失败: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return stats

    def check_dynamic_content_stability(self, page: Page, check_interval: int = 500, max_checks: int = 10) -> bool:
        """
        检查动态内容稳定性
        
        Args:
            page: Playwright页面对象
            check_interval: 检查间隔（毫秒）
            max_checks: 最大检查次数
            
        Returns:
            内容是否稳定
        """
        try:
            self.detection_steps.append("检查动态内容稳定性")
            start_time = time.time()
            
            previous_content = page.content()
            stable_count = 0
            
            for i in range(max_checks):
                time.sleep(check_interval / 1000)
                current_content = page.content()
                
                if current_content == previous_content:
                    stable_count += 1
                    if stable_count >= 3:
                        logger.info(f"动态内容已稳定（连续{stable_count}次检查无变化）")
                        elapsed = time.time() - start_time
                        logger.info(f"动态内容稳定性检测完成，耗时: {elapsed:.2f}秒")
                        return True
                else:
                    stable_count = 0
                    previous_content = current_content
            
            logger.warning(f"动态内容未在{max_checks}次检查内稳定")
            elapsed = time.time() - start_time
            logger.info(f"动态内容稳定性检测完成，耗时: {elapsed:.2f}秒")
            return False
        except Exception as e:
            error_msg = f"动态内容稳定性检测失败: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            return False

    def detect_page_load(self, page: Page, url: str, key_selectors: Optional[List[str]] = None) -> LoadDetectionResult:
        """
        执行完整的页面加载检测
        
        Args:
            page: Playwright页面对象
            url: 目标URL
            key_selectors: 关键元素选择器列表
            
        Returns:
            加载检测结果
        """
        self.detection_steps = []
        self.errors = []
        
        start_time = time.time()
        logger.info(f"开始检测页面加载: {url}")
        
        try:
            page.goto(url, wait_until='commit', timeout=self.timeout)
            
            success = True
            
            success &= self.wait_for_dom_ready(page)
            success &= self.wait_for_network_idle(page)
            
            if key_selectors:
                success &= self.check_element_visibility(page, key_selectors)
            
            image_stats = self.check_image_loading(page)
            success &= self.check_dynamic_content_stability(page)
            
            load_time = time.time() - start_time
            
            metrics = {
                'load_time': load_time,
                'image_loaded': image_stats['loaded'],
                'image_total': image_stats['total'],
                'image_success_rate': image_stats['loaded'] / image_stats['total'] if image_stats['total'] > 0 else 0
            }
            
            result = LoadDetectionResult(
                url=url,
                success=success,
                load_time=load_time,
                detection_steps=self.detection_steps,
                errors=self.errors,
                metrics=metrics
            )
            
            logger.info(f"页面加载检测完成，总耗时: {load_time:.2f}秒，成功: {success}")
            return result
            
        except Exception as e:
            error_msg = f"页面加载检测异常: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
            
            load_time = time.time() - start_time
            
            return LoadDetectionResult(
                url=url,
                success=False,
                load_time=load_time,
                detection_steps=self.detection_steps,
                errors=self.errors,
                metrics={}
            )


def main():
    """主函数 - 演示多维度页面加载检测"""
    from playwright.sync_api import sync_playwright
    
    logger.info("=" * 80)
    logger.info("Playwright多维度页面加载检测示例")
    logger.info("=" * 80)
    
    test_url = "https://www.example.com"
    key_selectors = ['h1', 'p']
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        detector = PageLoadDetector(timeout=30000)
        result = detector.detect_page_load(page, test_url, key_selectors)
        
        print("\n" + "=" * 80)
        print("检测结果报告")
        print("=" * 80)
        print(f"URL: {result.url}")
        print(f"加载状态: {'成功' if result.success else '失败'}")
        print(f"加载时间: {result.load_time:.2f}秒")
        print(f"\n检测步骤:")
        for i, step in enumerate(result.detection_steps, 1):
            print(f"  {i}. {step}")
        
        if result.errors:
            print(f"\n错误信息:")
            for error in result.errors:
                print(f"  - {error}")
        
        if result.metrics:
            print(f"\n性能指标:")
            for key, value in result.metrics.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")
        
        print("=" * 80)
        
        browser.close()


if __name__ == "__main__":
    main()
