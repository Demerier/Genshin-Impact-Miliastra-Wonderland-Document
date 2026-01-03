import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
import pytest

print("All dependencies installed successfully!")
print(f"requests version: {requests.__version__}")
print(f"beautifulsoup4 version: {BeautifulSoup.__version__}")
print(f"markdownify version: {markdownify.__version__}")
print(f"pytest version: {pytest.__version__}")
