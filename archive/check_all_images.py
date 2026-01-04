import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def check_all_images():
    """检查整个页面的所有图片，包括懒加载"""
    urls = [
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhz71urk21nq",  # 界面介绍
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhdtk89yhd6q",  # 概念介绍
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhsok60iqlxk",  # 节点介绍
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhoyplr76zr2",  # 辅助功能
        "https://act.mihoyo.com/ys/ugc/tutorial/detail/mhsumxr9cf3y",  # 附录
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for idx, url in enumerate(urls, 1):
            print(f"\n{'='*60}")
            print(f"[{idx}] {url}")
            print('='*60)
            
            try:
                await page.goto(url, wait_until="domcontentloaded")
                
                # 等待更长时间，让懒加载图片加载
                await page.wait_for_timeout(5000)
                
                # 滚动页面以触发懒加载
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
                html_content = await page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # 检查整个页面的图片
                all_images = soup.find_all('img')
                print(f"整个页面图片数量: {len(all_images)}")
                
                # 检查内容区域的图片
                content_div = soup.find('div', class_='doc-view')
                if content_div:
                    content_images = content_div.find_all('img')
                    print(f"内容区域图片数量: {len(content_images)}")
                    
                    if content_images:
                        print("\n内容区域图片详情:")
                        for i, img in enumerate(content_images[:5], 1):
                            src = img.get('src', '')
                            data_src = img.get('data-src', '')
                            alt = img.get('alt', '')
                            print(f"  [{i}] src: {src[:80] if src else '(空)'}")
                            print(f"      data-src: {data_src[:80] if data_src else '(空)'}")
                            print(f"      alt: {alt}")
                else:
                    print("未找到内容区域")
                
                # 检查是否有背景图
                print("\n检查背景图:")
                elements_with_bg = soup.find_all(style=True)
                bg_count = 0
                for el in elements_with_bg[:10]:
                    style = el.get('style', '')
                    if 'background-image' in style or 'background' in style:
                        bg_count += 1
                        if bg_count <= 3:
                            print(f"  [{bg_count}] {el.name}: {style[:100]}")
                print(f"共找到 {bg_count} 个包含背景图的元素")
                
            except Exception as e:
                print(f"错误: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_all_images())
