#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/bytedance/trading/asr_project')

from download_from_url import get_episode_info, sanitize_filename

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

try:
    audio_url, title = get_episode_info(test_url)
    print(f'✅ 找到节目标题: {title}')
    print(f'✅ 找到音频 URL: {audio_url}')
    
    # 测试文件名清理
    clean_title = sanitize_filename(title)
    filename = f'{clean_title}.m4a'
    print(f'\n清理后的文件名: {filename}')
    
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
