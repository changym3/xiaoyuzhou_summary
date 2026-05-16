#!/usr/bin/env python3
import requests

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(test_url, headers=headers)
print(f"状态码: {response.status_code}")
print(f"\nHTML 内容前 2000 字符:\n{response.text[:2000]}")

# 查找所有 meta 标签
import re
meta_tags = re.findall(r'<meta[^>]+>', response.text)
print(f"\n找到 {len(meta_tags)} 个 meta 标签:")
for tag in meta_tags:
    if 'og:' in tag or 'audio' in tag.lower():
        print(f"  {tag}")
