import os
from pathlib import Path

images_dir = Path("data/images_trial")
if images_dir.exists():
    for png_file in images_dir.glob("*.png"):
        print(f"删除: {png_file}")
        os.remove(png_file)
    print("清理完成")
else:
    print("目录不存在")
