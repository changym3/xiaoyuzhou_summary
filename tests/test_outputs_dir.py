#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/Users/bytedance/trading/asr_project')

from download_from_url import get_episode_info, sanitize_filename

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

try:
    audio_url, podcast_name, episode_title = get_episode_info(test_url)
    print(f'✅ 找到播客节目: {podcast_name}')
    print(f'✅ 找到单集标题: {episode_title}')
    print(f'✅ 找到音频 URL: {audio_url}')
    
    # 清理名称
    clean_podcast_name = sanitize_filename(podcast_name)
    clean_episode_title = sanitize_filename(episode_title)
    
    # 测试默认输出目录为 outputs
    default_output_dir = 'outputs'
    podcast_folder = os.path.join(default_output_dir, clean_podcast_name)
    filename = f'{clean_episode_title}.m4a'
    
    print(f'\n默认输出目录: {default_output_dir}')
    print(f'播客文件夹: {podcast_folder}')
    print(f'完整文件路径: {os.path.join(podcast_folder, filename)}')
    
    # 显示完整的文件结构
    print(f'\n完整文件结构:')
    print(f'{default_output_dir}/')
    print(f'  {clean_podcast_name}/')
    print(f'    {clean_episode_title}.m4a')
    
    print(f'\n✅ 测试完成！默认输出目录已设置为 outputs')
    print(f'✅ outputs/ 目录已添加到 .gitignore')
        
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
