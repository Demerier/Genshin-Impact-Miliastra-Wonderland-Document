import re
import json
from pathlib import Path
from collections import defaultdict

class QualityAudit:
    def __init__(self, markdown_dir):
        self.markdown_dir = Path(markdown_dir)
        self.issues = defaultdict(list)
        self.stats = {
            'total_files': 0,
            'files_with_issues': 0,
            'cdn_links': 0,
            'nested_images': 0,
            'text_inserted_images': 0,
            'corrupted_text': 0,
            'empty_images': 0,
            'header_images': 0
        }
    
    def audit_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_issues = []
        
        pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            alt_text = match.group(1)
            img_url = match.group(2)
            line_num = content[:match.start()].count('\n') + 1
            
            if img_url.startswith('http'):
                file_issues.append({
                    'type': 'cdn_link',
                    'line': line_num,
                    'url': img_url,
                    'description': '使用CDN链接而非本地路径'
                })
                self.stats['cdn_links'] += 1
            
            if alt_text and len(alt_text) > 100:
                file_issues.append({
                    'type': 'corrupted_text',
                    'line': line_num,
                    'description': f'图片alt文本异常长: {alt_text[:50]}...'
                })
                self.stats['corrupted_text'] += 1
            
            if not alt_text and not img_url:
                file_issues.append({
                    'type': 'empty_image',
                    'line': line_num,
                    'description': '空图片引用'
                })
                self.stats['empty_images'] += 1
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if '![]()' in line and len(line) > 10:
                file_issues.append({
                    'type': 'text_inserted_image',
                    'line': i,
                    'description': f'图片插入在文本中: {line[:50]}...'
                })
                self.stats['text_inserted_images'] += 1
            
            if '![](' in line and '![](' in line[line.find('![](')+4:]:
                file_issues.append({
                    'type': 'nested_image',
                    'line': i,
                    'description': f'嵌套图片引用: {line[:50]}...'
                })
                self.stats['nested_images'] += 1
            
            if '说!' in line or '说明!' in line:
                file_issues.append({
                    'type': 'corrupted_text',
                    'line': i,
                    'description': f'文本损坏: {line[:50]}...'
                })
                self.stats['corrupted_text'] += 1
        
        if file_issues:
            self.issues[file_path.name] = file_issues
            self.stats['files_with_issues'] += 1
        
        return file_issues
    
    def audit_all(self):
        md_files = list(self.markdown_dir.glob('*.md'))
        self.stats['total_files'] = len(md_files)
        
        for md_file in md_files:
            self.audit_file(md_file)
        
        return self.issues, self.stats
    
    def generate_report(self, output_path):
        report = {
            'summary': self.stats,
            'detailed_issues': dict(self.issues)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report

if __name__ == '__main__':
    markdown_dir = Path('data/markdown')
    output_dir = Path('.trae/documents')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    auditor = QualityAudit(markdown_dir)
    issues, stats = auditor.audit_all()
    
    print(f"质量审计完成")
    print(f"总文件数: {stats['total_files']}")
    print(f"有问题的文件: {stats['files_with_issues']}")
    print(f"CDN链接: {stats['cdn_links']}")
    print(f"嵌套图片: {stats['nested_images']}")
    print(f"文本插入图片: {stats['text_inserted_images']}")
    print(f"文本损坏: {stats['corrupted_text']}")
    print(f"空图片: {stats['empty_images']}")
    
    report_path = output_dir / 'quality_audit_report.json'
    auditor.generate_report(report_path)
    print(f"\n详细报告已保存至: {report_path}")
