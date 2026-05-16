#!/usr/bin/env python3
import requests
import re

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(test_url, headers=headers)
response.raise_for_status()

# 查找 title 标签
title_pattern = r'<title>([^<]+)</title>'
title_match = re.search(title_pattern, response.text)
if title_match:
    print(f"title 标签: {title_match.group(1)}")

# 查找 og:title 标签
og_title_pattern = r'<meta\s+property="og:title"\s+content="([^"]+)"\s*/?>'
og_title_match = re.search(og_title_pattern, response.text)
if og_title_match:
    print(f"og:title 标签: {og_title_match.group(1)}")

# 查找 schema:podcast-show 里的 name
schema_pattern = r'"name":"([^"]+)"'
schema_matches = re.findall(schema_pattern, response.text)
print(f"\nschema 中的 name: {schema_matches[:5]}")
