import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def inspect_images():
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
        
        content_div = soup.find('div', class_='doc-view')
        
        if content_div:
            print("=== 找到内容区域 (.doc-view) ===")
            print(f"内容区域HTML长度: {len(str(content_div))}")
            
            print("\n=== 查找所有图片 ===")
            found_count = 0
            for img_tag in content_div.find_all('img'):
                found_count += 1
                src = img_tag.get('src', '')
                data_src = img_tag.get('data-src', '')
                alt = img_tag.get('alt', '')
                print(f"\n[{found_count}] 图片:")
                print(f"  src: {src[:100]}")
                print(f"  data-src: {data_src[:100]}")
                print(f"  alt: {alt}")
                
                # 获取父元素文本
                parent = img_tag.parent
                if parent:
                    parent_text = parent.get_text(strip=True)[:100]
                    print(f"  父元素文本: {parent_text}")
                print("-" * 50)
            
            if found_count == 0:
                print("未找到图片标签")
                print("\n=== 显示前1000个字符的HTML ===")
                print(str(content_div)[:1000])
        else:
            print("未找到.doc-view内容区域")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_images())
