import os
import shutil
import glob

# 定义源文件模式和目标目录
source_patterns = [
    "check_*.py",
    "clean_*.py", 
    "trial_*.py",
    "run_*.py",
    "find_*.py",
    "inspect_*.py"
]
dest_dir = "archive"

# 创建目标目录（如果不存在）
os.makedirs(dest_dir, exist_ok=True)

# 移动所有匹配的文件
for pattern in source_patterns:
    for file_path in glob.glob(pattern):
        if os.path.exists(file_path):
            dest_path = os.path.join(dest_dir, os.path.basename(file_path))
            shutil.move(file_path, dest_path)
            print(f"已移动: {file_path} -> {dest_path}")

print("文件移动完成！")