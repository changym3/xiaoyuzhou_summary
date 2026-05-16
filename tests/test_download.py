#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/bytedance/trading/asr_project/references/xiaoyuzhou-podcast/scripts')

from download_from_url import get_audio_url
import requests
import os

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

try:
    audio_url = get_audio_url(test_url)
    print(f"✅ 成功提取音频 URL: {audio_url}")
    
    # 只下载前 100KB 来测试
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Range': 'bytes=0-102400'
    }
    
    print("\n正在测试下载（仅前 100KB）...")
    response = requests.get(audio_url, headers=headers, stream=True)
    response.raise_for_status()
    
    test_file = "test_audio_part.m4a"
    with open(test_file, 'wb') as f:
        f.write(response.content)
    
    file_size = os.path.getsize(test_file)
    print(f"✅ 下载测试成功！文件大小: {file_size} 字节")
    print(f"✅ 文件保存为: {test_file}")
    
except Exception as e:
    print(f"❌ 失败: {e}")
    import traceback
    traceback.print_exc()
