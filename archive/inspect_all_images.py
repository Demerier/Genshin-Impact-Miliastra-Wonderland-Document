import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def inspect_all_images():
    """检查整个页面中的所有图片"""
    url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("正在加载页面...")
        await page.goto(url, wait_until="domcontentloaded")
        
        print("等待内容加载...")
        try:
            await page.wait_for_selector('.doc-view', timeout=15000)
        except:
            print("等待.doc-view超时，继续处理...")
        
        await page.wait_for_timeout(5000)
        
        html_content = await page.content()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("\n=== 检查整个页面的所有图片 ===")
        all_images = soup.find_all('img')
        print(f"整个页面共找到 {len(all_images)} 个图片标签\n")
        
        for idx, img_tag in enumerate(all_images, 1):
            src = img_tag.get('src', '')
            data_src = img_tag.get('data-src', '')
            alt = img_tag.get('alt', '')
            class_attr = img_tag.get('class', [])
            
            print(f"[{idx}] 图片:")
            print(f"  src: {src[:100] if src else '(空)'}")
            print(f"  data-src: {data_src[:100] if data_src else '(空)'}")
            print(f"  alt: {alt}")
            print(f"  class: {class_attr}")
            
            # 检查是否在.doc-view区域内
            parent = img_tag.find_parent('div', class_='doc-view')
            if parent:
                print(f"  位置: 在内容区域 (.doc-view) 内")
            else:
                print(f"  位置: 不在内容区域内")
            
            # 获取父元素信息
            parent = img_tag.parent
            if parent:
                parent_class = parent.get('class', [])
                parent_id = parent.get('id', '')
                print(f"  父元素 class: {parent_class}")
                print(f"  父元素 id: {parent_id}")
            
            print("-" * 60)
        
        print("\n=== 检查内容区域 ===")
        content_div = soup.find('div', class_='doc-view')
        if content_div:
            content_images = content_div.find_all('img')
            print(f"内容区域 (.doc-view) 内的图片数量: {len(content_images)}")
        else:
            print("未找到内容区域 (.doc-view)")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_all_images())
