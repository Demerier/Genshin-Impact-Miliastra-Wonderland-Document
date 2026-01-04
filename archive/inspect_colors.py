import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def inspect_colors():
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
            
            print("\n=== 查找所有带有颜色的元素 ===")
            found_count = 0
            for elem in content_div.find_all(['span', 'strong', 'em', 'i', 'b', 'font', 'p', 'div']):
                style = elem.get('style', '')
                class_name = elem.get('class', [])
                
                if style or class_name:
                    text = elem.get_text(strip=True)
                    if text and len(text) > 3:
                        found_count += 1
                        print(f"\n[{found_count}] 标签: {elem.name}")
                        print(f"文本: {text[:80]}")
                        print(f"Style: {style}")
                        print(f"Class: {class_name}")
                        print(f"HTML: {str(elem)[:200]}")
                        print("-" * 50)
            
            if found_count == 0:
                print("未找到带有style或class的元素")
                print("\n=== 显示前1000个字符的HTML ===")
                print(str(content_div)[:1000])
        else:
            print("未找到.doc-view内容区域")
            print("\n=== 查找所有可能的容器 ===")
            for div in soup.find_all('div'):
                class_name = div.get('class', [])
                if class_name:
                    class_str = ' '.join(class_name)
                    if any(keyword in class_str.lower() for keyword in ['doc', 'content', 'view', 'article', 'main']):
                        print(f"找到div: class={class_name}")
                        print(f"HTML片段: {str(div)[:300]}")
                        print("-" * 30)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_colors())
