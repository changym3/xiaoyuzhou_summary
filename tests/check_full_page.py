#!/usr/bin/env python3
import requests
import re

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(test_url, headers=headers)
response.raise_for_status()

print(f"状态码: {response.status_code}")
print(f"\n=== HTML 前 5000 字符 ===")
print(response.text[:5000])

print(f"\n\n=== 查找所有相关的 meta 标签 ===")
# 查找所有 meta 标签
meta_tags = re.findall(r'<meta[^>]+>', response.text)
for tag in meta_tags:
    print(f"  {tag}")

print(f"\n\n=== 查找 title 标签 ===")
title_tag = re.search(r'<title[^>]*>([^<]+)</title>', response.text)
if title_tag:
    print(f"  Title: {title_tag.group(1)}")

print(f"\n\n=== 查找所有可能包含播客/节目信息的内容 ===")
# 查找 JSON-LD 或其他结构化数据
json_ld = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', response.text, re.DOTALL)
for i, data in enumerate(json_ld):
    print(f"\nJSON-LD #{i}:")
    print(data[:2000])
