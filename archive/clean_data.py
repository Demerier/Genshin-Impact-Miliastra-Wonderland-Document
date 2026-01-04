import os
import shutil
from pathlib import Path

def clean_data():
    """清理现有爬取数据"""
    print("=" * 80)
    print("开始清理现有爬取数据")
    print("=" * 80)
    print()

    # 定义需要清理的目录
    data_dir = Path("data")
    images_dir = data_dir / "images"
    markdown_dir = data_dir / "markdown"
    html_dir = data_dir / "html"
    resume_file = data_dir / "crawl_resume.json"

    # 清理图片目录
    if images_dir.exists():
        image_count = len(list(images_dir.glob("*.png")))
        print(f"清理图片目录: {images_dir}")
        print(f"  删除图片数量: {image_count}")
        shutil.rmtree(images_dir)
        images_dir.mkdir(parents=True, exist_ok=True)
        print("  ✓ 图片目录已清理")
    else:
        print(f"图片目录不存在: {images_dir}")
    print()

    # 清理Markdown目录
    if markdown_dir.exists():
        markdown_count = len(list(markdown_dir.glob("*.md")))
        print(f"清理Markdown目录: {markdown_dir}")
        print(f"  删除文件数量: {markdown_count}")
        shutil.rmtree(markdown_dir)
        markdown_dir.mkdir(parents=True, exist_ok=True)
        print("  ✓ Markdown目录已清理")
    else:
        print(f"Markdown目录不存在: {markdown_dir}")
    print()

    # 清理HTML目录
    if html_dir.exists():
        html_count = len(list(html_dir.glob("*.html")))
        print(f"清理HTML目录: {html_dir}")
        print(f"  删除文件数量: {html_count}")
        shutil.rmtree(html_dir)
        html_dir.mkdir(parents=True, exist_ok=True)
        print("  ✓ HTML目录已清理")
    else:
        print(f"HTML目录不存在: {html_dir}")
    print()

    # 清理恢复文件
    if resume_file.exists():
        print(f"清理恢复文件: {resume_file}")
        resume_file.unlink()
        print("  ✓ 恢复文件已删除")
    else:
        print(f"恢复文件不存在: {resume_file}")
    print()

    print("=" * 80)
    print("数据清理完成")
    print("=" * 80)

if __name__ == "__main__":
    clean_data()
