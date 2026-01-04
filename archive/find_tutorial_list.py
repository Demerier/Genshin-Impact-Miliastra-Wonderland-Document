import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def find_tutorial_list():
    """查找教程列表"""
    list_url = "https://act.mihoyo.com/ys/ugc/tutorial"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("正在加载教程列表页...")
        await page.goto(list_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print("=== 查找所有教程卡片 ===")
        
        # 查找所有教程链接
        tutorial_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag.get('href', '')
            if '/detail/' in href:
                doc_id = href.split('/detail/')[-1].split('?')[0]
                full_url = f"https://act.mihoyo.com/ys/ugc/tutorial/detail/{doc_id}"
                link_text = a_tag.get_text(strip=True)
                
                if link_text and full_url not in [l['url'] for l in tutorial_links]:
                    tutorial_links.append({
                        'url': full_url,
                        'doc_id': doc_id,
                        'name': link_text
                    })
        
        print(f"共找到 {len(tutorial_links)} 个教程")
        
        # 检查前10个教程的图片情况
        print("\n=== 检查前10个教程的图片情况 ===")
        for i, link in enumerate(tutorial_links[:10], 1):
            print(f"\n[{i}] {link['name']}")
            print(f"    URL: {link['url']}")
            
            try:
                await page.goto(link['url'], wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)
                
                # 滚动页面以触发懒加载
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                
                page_html = await page.content()
                page_soup = BeautifulSoup(page_html, 'html.parser')
                page_content = page_soup.find('div', class_='doc-view')
                
                if page_content:
                    images = page_content.find_all('img')
                    print(f"    内容区域图片数量: {len(images)}")
                    if images:
                        for idx, img in enumerate(images[:3], 1):
                            src = img.get('src', '') or img.get('data-src', '')
                            alt = img.get('alt', '')
                            print(f"      图片{idx}: {src[:80]}... (alt: {alt[:30]})")
            except Exception as e:
                print(f"    错误: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(find_tutorial_list())
