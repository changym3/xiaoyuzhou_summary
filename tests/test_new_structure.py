#!/usr/bin/env python3
import sys
import os
import tempfile
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
    
    print(f'\n清理后的播客节目名: {clean_podcast_name}')
    print(f'清理后的单集标题: {clean_episode_title}')
    
    # 测试文件夹结构
    test_output_dir = tempfile.mkdtemp(prefix='test_podcast_')
    podcast_folder = os.path.join(test_output_dir, clean_podcast_name)
    filename = f'{clean_episode_title}.m4a'
    
    print(f'\n测试输出目录: {test_output_dir}')
    print(f'播客文件夹: {podcast_folder}')
    print(f'完整文件路径: {os.path.join(podcast_folder, filename)}')
    
    # 创建文件夹
    os.makedirs(podcast_folder, exist_ok=True)
    print(f'\n✅ 文件夹创建成功: {podcast_folder}')
    print(f'✅ 文件夹存在: {os.path.exists(podcast_folder)}')
    
    # 创建一个小的测试文件
    test_file_path = os.path.join(podcast_folder, 'test.txt')
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(f'播客节目: {podcast_name}\n')
        f.write(f'单集标题: {episode_title}\n')
        f.write(f'音频URL: {audio_url}\n')
    
    print(f'✅ 测试文件创建成功: {test_file_path}')
    print(f'\n测试完成！文件夹结构已验证。')
    
    # 打印文件夹内容
    print(f'\n文件夹内容:')
    for item in os.listdir(podcast_folder):
        print(f'  - {item}')
    
    # 显示完整的文件结构
    print(f'\n完整文件结构:')
    print(f'{test_output_dir}/')
    print(f'  {clean_podcast_name}/')
    print(f'    {clean_episode_title}.m4a')
        
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
