#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/bytedance/trading/asr_project/references/xiaoyuzhou-podcast/scripts')

from download_from_url import get_audio_url

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

try:
    audio_url = get_audio_url(test_url)
    print(f"✅ 成功提取音频 URL: {audio_url}")
except Exception as e:
    print(f"❌ 失败: {e}")
    import traceback
    traceback.print_exc()
