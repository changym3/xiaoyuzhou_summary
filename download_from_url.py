#!/usr/bin/env python3
import argparse
import requests
import re
import os
import json
from urllib.parse import urlparse


def sanitize_filename(filename):
    """清理文件名中的特殊字符"""
    # 替换文件名中不允许的字符
    invalid_chars = r'[<>:"/\\|?*]'
    filename = re.sub(invalid_chars, '_', filename)
    # 替换中文引号
    filename = filename.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    # 去除首尾空白
    filename = filename.strip()
    # 限制文件名长度（防止过长）
    if len(filename) > 100:
        filename = filename[:100].strip()
    return filename


def get_episode_info(page_url):
    """从页面获取音频URL、播客节目名称和单集标题"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()
    
    # 提取音频URL
    audio_pattern = r'<meta\s+property="og:audio"\s+content="([^"]+)"\s*/?>'
    audio_match = re.search(audio_pattern, response.text)
    if not audio_match:
        raise ValueError('未找到 og:audio 标签')
    audio_url = audio_match.group(1)
    
    # 从 JSON-LD 中获取播客节目名称和单集标题
    json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    json_ld_match = re.search(json_ld_pattern, response.text, re.DOTALL)
    
    podcast_name = 'podcast'
    episode_title = 'episode'
    
    if json_ld_match:
        try:
            data = json.loads(json_ld_match.group(1))
            # 获取单集标题
            if 'name' in data:
                episode_title = data['name']
            # 获取播客节目名称
            if 'partOfSeries' in data and 'name' in data['partOfSeries']:
                podcast_name = data['partOfSeries']['name']
        except (json.JSONDecodeError, KeyError):
            # 如果 JSON 解析失败，回退到 og:title
            title_pattern = r'<meta\s+property="og:title"\s+content="([^"]+)"\s*/?>'
            title_match = re.search(title_pattern, response.text)
            if title_match:
                episode_title = title_match.group(1)
    
    return audio_url, podcast_name, episode_title


def download_file(url, output_dir='.', filename=None):
    """下载文件，可指定文件名"""
    if filename is None:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = 'audio.m4a'
    
    output_path = os.path.join(output_dir, filename)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f'正在下载: {url}')
    print(f'保存到: {output_path}')
    
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f'\r下载进度: {percent:.1f}%', end='')
    
    print(f'\n✅ 下载完成: {output_path}')
    return output_path


def main():
    parser = argparse.ArgumentParser(description='从小宇宙播客页面下载 m4a 音频文件')
    parser.add_argument('url', help='小宇宙播客单集页面 URL')
    parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录（默认：outputs）')
    
    args = parser.parse_args()
    
    try:
        audio_url, podcast_name, episode_title = get_episode_info(args.url)
        print(f'找到播客节目: {podcast_name}')
        print(f'找到单集标题: {episode_title}')
        print(f'找到音频 URL: {audio_url}')
        
        # 清理名称
        clean_podcast_name = sanitize_filename(podcast_name)
        clean_episode_title = sanitize_filename(episode_title)
        
        # 创建播客节目文件夹
        podcast_folder = os.path.join(args.output_dir, clean_podcast_name)
        filename = f'{clean_episode_title}.m4a'
        
        os.makedirs(podcast_folder, exist_ok=True)
        print(f'创建播客文件夹: {podcast_folder}')
        
        # 下载音频到播客文件夹
        download_file(audio_url, podcast_folder, filename)
        
    except Exception as e:
        print(f'❌ 错误: {e}')
        exit(1)


if __name__ == '__main__':
    main()
