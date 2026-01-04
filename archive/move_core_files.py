import os
import shutil

# 定义核心文件和目标目录映射
core_files = {
    "crawler.py": "src/crawler/",
    "crawl_config.py": "src/crawler/",
    "knowledge_service.py": "src/knowledge/",
    "knowledge_repository.py": "src/knowledge/",
    "knowledge_models.py": "src/knowledge/",
    "knowledge_base.py": "src/knowledge/",
    "document_parser.py": "src/knowledge/",
    "ai_adapter.py": "src/knowledge/",
    "ai_agent.py": "src/knowledge/",
    "prompt_generator.py": "src/knowledge/",
    "main.py": "src/api/"
}

# 移动所有核心文件
for file_path, dest_dir in core_files.items():
    if os.path.exists(file_path):
        dest_path = os.path.join(dest_dir, os.path.basename(file_path))
        shutil.move(file_path, dest_path)
        print(f"已移动: {file_path} -> {dest_path}")

print("核心文件移动完成！")