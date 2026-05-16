#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/Users/bytedance/trading/asr_project')

from download_from_url import get_episode_info, sanitize_filename, download_file
import tempfile

test_url = "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

try:
    audio_url, title = get_episode_info(test_url)
    print(f'✅ 找到节目标题: {title}')
    print(f'✅ 找到音频 URL: {audio_url}')
    
    # 清理标题
    clean_title = sanitize_filename(title)
    print(f'\n清理后的标题: {clean_title}')
    
    # 测试文件夹创建逻辑
    test_output_dir = tempfile.mkdtemp(prefix='test_podcast_')
    episode_folder = os.path.join(test_output_dir, clean_title)
    filename = f'{clean_title}.m4a'
    
    print(f'\n测试输出目录: {test_output_dir}')
    print(f'节目文件夹路径: {episode_folder}')
    print(f'完整文件路径: {os.path.join(episode_folder, filename)}')
    
    # 只测试创建文件夹，不下载完整文件
    os.makedirs(episode_folder, exist_ok=True)
    print(f'\n✅ 文件夹创建测试成功: {episode_folder}')
    print(f'✅ 文件夹存在: {os.path.exists(episode_folder)}')
    
    # 创建一个小的测试文件
    test_file_path = os.path.join(episode_folder, 'test.txt')
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(f'测试文件: {title}\n')
        f.write(f'音频URL: {audio_url}\n')
    
    print(f'✅ 测试文件创建成功: {test_file_path}')
    print(f'\n测试完成！文件夹结构已验证。')
    
    # 打印文件夹内容
    print(f'\n文件夹内容:')
    for item in os.listdir(episode_folder):
        print(f'  - {item}')
        
except Exception as e:
    print(f'❌ 错误: {e}')
    import traceback
    traceback.print_exc()
