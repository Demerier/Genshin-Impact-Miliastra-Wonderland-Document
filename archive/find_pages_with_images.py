import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def find_pages_with_images():
    """查找包含图片的页面"""
    base_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/"
    
    # 从主页获取所有链接
    start_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/mh29wpicgvh0"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("正在加载主页...")
        await page.goto(start_url, wait_until="domcontentloaded")
        
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
            print("=== 提取所有教程链接 ===")
            links = []
            for a_tag in content_div.find_all('a', href=True):
                href = a_tag.get('href', '')
                if '/detail/' in href:
                    # 提取文档ID
                    doc_id = href.split('/detail/')[-1].split('?')[0]
                    link_text = a_tag.get_text(strip=True)
                    full_url = f"{base_url}{doc_id}"
                    links.append({
                        'url': full_url,
                        'doc_id': doc_id,
                        'name': link_text
                    })
                    print(f"  - {link_text}: {full_url}")
            
            print(f"\n共找到 {len(links)} 个链接")
            
            # 检查前5个页面是否包含图片
            print("\n=== 检查前5个页面的图片情况 ===")
            for i, link in enumerate(links[:5], 1):
                print(f"\n[{i}] {link['name']}")
                print(f"    URL: {link['url']}")
                
                try:
                    await page.goto(link['url'], wait_until="domcontentloaded")
                    await page.wait_for_timeout(3000)
                    
                    page_html = await page.content()
                    page_soup = BeautifulSoup(page_html, 'html.parser')
                    page_content = page_soup.find('div', class_='doc-view')
                    
                    if page_content:
                        images = page_content.find_all('img')
                        print(f"    图片数量: {len(images)}")
                        if images:
                            for idx, img in enumerate(images[:3], 1):
                                src = img.get('src', '') or img.get('data-src', '')
                                alt = img.get('alt', '')
                                print(f"      图片{idx}: {src[:80]}... (alt: {alt[:30]})")
                except Exception as e:
                    print(f"    错误: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(find_pages_with_images())
