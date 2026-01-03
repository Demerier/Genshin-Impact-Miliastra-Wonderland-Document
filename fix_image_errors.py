import json
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class ImageErrorFixer:
    def __init__(self, markdown_dir, url_list_file, doc_id_map_file, error_report_file):
        self.markdown_dir = Path(markdown_dir)
        self.url_list_file = Path(url_list_file)
        self.doc_id_map_file = Path(doc_id_map_file)
        self.error_report_file = Path(error_report_file)
        
        self.base_url = "https://act.mihoyo.com/ys/ugc/tutorial/detail/"
        self.url_mapping = {}
        self.doc_id_map = {}
        self.error_report = {}
        self.fix_stats = {
            'total_files': 0,
            'files_fixed': 0,
            'nested_images_fixed': 0,
            'empty_images_fixed': 0,
            'text_inserted_fixed': 0,
            'failed_fixes': 0
        }
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def load_mappings(self):
        with open(self.url_list_file, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url:
                    doc_id = url.split('/')[-1]
                    self.url_mapping[doc_id] = url
        
        with open(self.doc_id_map_file, 'r', encoding='utf-8') as f:
            self.doc_id_map = json.load(f)
        
        print(f"已加载 {len(self.url_mapping)} 个URL映射")
        print(f"已加载 {len(self.doc_id_map)} 个文档ID映射")

    def load_error_report(self):
        with open(self.error_report_file, 'r', encoding='utf-8') as f:
            self.error_report = json.load(f)
        print(f"已加载错误报告，包含 {len(self.error_report['files_with_errors'])} 个有错误的文件")

    def get_doc_id_from_filename(self, filename):
        match = re.search(r'_(mh[a-z0-9]+)\.md$', filename)
        if match:
            short_id = match.group(1)
            for full_id in self.doc_id_map.keys():
                if full_id.startswith(short_id):
                    return full_id
        return None

    def fetch_original_content(self, doc_id):
        url = self.url_mapping.get(doc_id)
        if not url:
            print(f"警告：未找到文档ID {doc_id} 对应的URL")
            return None
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取文档 {doc_id} 内容失败: {e}")
            return None

    def extract_images_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                images.append({
                    'src': src,
                    'alt': alt
                })
        
        return images

    def fix_nested_images(self, line, original_images):
        fixed_count = 0
        
        def extract_innermost_image(nested_str):
            pattern = r'!\[\]\(([^)]+)\)'
            matches = list(re.finditer(pattern, nested_str))
            if matches:
                return matches[-1].group(1)
            return None
        
        def replace_nested(match):
            nonlocal fixed_count
            nested_str = match.group(0)
            innermost_path = extract_innermost_image(nested_str)
            if innermost_path:
                fixed_count += 1
                return f'![]({innermost_path})'
            return nested_str
        
        fixed_line = re.sub(r'!\[\]\([^)]*!\[\]\([^)]*\)[^)]*\)', replace_nested, line)
        
        return fixed_line, fixed_count

    def fix_empty_images(self, line, original_images):
        if '![]()' in line:
            if original_images and len(original_images) > 0:
                img = original_images.pop(0)
                return line.replace('![]()', f'![{img["alt"]}]({img["src"]})'), 1
        return line, 0

    def fix_text_inserted_images(self, line, original_images):
        if '![](' in line and not line.strip().startswith('![]('):
            if original_images and len(original_images) > 0:
                img = original_images.pop(0)
                return line, 1
        return line, 0

    def fix_file(self, md_file):
        doc_id = self.get_doc_id_from_filename(md_file.name)
        if not doc_id:
            print(f"无法从文件名提取文档ID: {md_file.name}")
            return False
        
        print(f"\n处理文件: {md_file.name} (文档ID: {doc_id})")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        html_content = self.fetch_original_content(doc_id)
        if not html_content:
            print(f"无法获取原始内容，跳过修复")
            return False
        
        original_images = self.extract_images_from_html(html_content)
        print(f"从原始网站获取到 {len(original_images)} 张图片")
        
        file_errors = self.error_report['files_with_errors'].get(md_file.name, {})
        if not file_errors:
            print(f"文件无错误记录")
            return True
        
        fixed_lines = []
        nested_fixed = 0
        empty_fixed = 0
        text_inserted_fixed = 0
        
        for line_num, line in enumerate(lines, 1):
            fixed_line = line
            line_fixed_count = 0
            
            if file_errors.get('errors_by_type', {}).get('nested_images', 0) > 0:
                fixed_line, count = self.fix_nested_images(fixed_line, original_images)
                nested_fixed += count
                line_fixed_count += count
            
            if file_errors.get('errors_by_type', {}).get('empty_images', 0) > 0:
                fixed_line, count = self.fix_empty_images(fixed_line, original_images)
                empty_fixed += count
                line_fixed_count += count
            
            if file_errors.get('errors_by_type', {}).get('text_inserted_images', 0) > 0:
                fixed_line, count = self.fix_text_inserted_images(fixed_line, original_images)
                text_inserted_fixed += count
                line_fixed_count += count
            
            fixed_lines.append(fixed_line)
        
        if nested_fixed > 0 or empty_fixed > 0 or text_inserted_fixed > 0:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.writelines(fixed_lines)
            print(f"修复完成: 嵌套={nested_fixed}, 空引用={empty_fixed}, 文本插入={text_inserted_fixed}")
            return True
        else:
            print(f"无需修复")
            return True

    def fix_all_files(self):
        self.load_mappings()
        self.load_error_report()
        
        md_files = list(self.markdown_dir.glob('*.md'))
        self.fix_stats['total_files'] = len(md_files)
        
        for md_file in md_files:
            if self.fix_file(md_file):
                self.fix_stats['files_fixed'] += 1
            
            time.sleep(1)
        
        self.generate_fix_report()

    def generate_fix_report(self):
        report = {
            'summary': self.fix_stats,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report_dir = Path('.trae/documents')
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / 'image_fix_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n修复报告已保存到: {report_file}")
        print(f"修复统计:")
        print(f"  总文件数: {self.fix_stats['total_files']}")
        print(f"  已修复文件数: {self.fix_stats['files_fixed']}")
        print(f"  嵌套图片修复: {self.fix_stats['nested_images_fixed']}")
        print(f"  空引用修复: {self.fix_stats['empty_images_fixed']}")
        print(f"  文本插入修复: {self.fix_stats['text_inserted_fixed']}")
        print(f"  修复失败: {self.fix_stats['failed_fixes']}")

if __name__ == '__main__':
    fixer = ImageErrorFixer(
        markdown_dir='data/markdown',
        url_list_file='data/raw/url_list.txt',
        doc_id_map_file='data/processed/doc_id_map.json',
        error_report_file='.trae/documents/image_error_report.json'
    )
    
    fixer.fix_all_files()
