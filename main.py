#!/usr/bin/env python3
import argparse
import os
from download_from_url import get_episode_info, download_file, sanitize_filename
from transcribe_audio import transcribe_audio


def main():
    parser = argparse.ArgumentParser(description='ASR 项目：播客下载与语音转写（统一调度入口')
    subparsers = parser.add_subparsers(title='子命令', dest='command', help='可用命令')
    
    # 下载子命令
    download_parser = subparsers.add_parser('download', help='下载播客音频（仅下载')
    download_parser.add_argument('url', help='小宇宙播客单集页面 URL')
    download_parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录（默认：outputs）')
    download_parser.add_argument('--transcribe', action='store_true', help='下载后自动转写')
    download_parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                               help='转写模型大小（默认：small）')
    download_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                               help='计算设备（默认：cpu）')
    download_parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                               help='计算类型（默认：int8）')
    download_parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json'],
                               choices=['txt', 'srt', 'json'],
                               help='转写输出格式（默认：txt srt json）')
    
    # 转写子命令
    transcribe_parser = subparsers.add_parser('transcribe', help='转写音频文件（仅转写）')
    transcribe_parser.add_argument('audio_path', help='音频文件路径')
    transcribe_parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                                 help='转写模型大小（默认：small）')
    transcribe_parser.add_argument('--language', default='zh', help='语言代码（默认：zh）')
    transcribe_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                                 help='计算设备（默认：cpu）')
    transcribe_parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                                 help='计算类型（默认：int8）')
    transcribe_parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json'],
                                 choices=['txt', 'srt', 'json'],
                                 help='输出格式（默认：txt srt json）')
    transcribe_parser.add_argument('--output-dir', help='输出目录（默认同音频目录）')
    transcribe_parser.add_argument('--no-word-timestamps', action='store_true', help='不输出词级时间戳')
    transcribe_parser.add_argument('--no-vad-filter', action='store_true', help='不使用 VAD 过滤静音')
    
    args = parser.parse_args()
    
    if args.command == 'download':
        try:
            # 仅负责下载
            audio_url, podcast_name, episode_title = get_episode_info(args.url)
            print(f'找到播客节目: {podcast_name}')
            print(f'找到单集标题: {episode_title}')
            print(f'找到音频 URL: {audio_url}')
            
            clean_podcast_name = sanitize_filename(podcast_name)
            clean_episode_title = sanitize_filename(episode_title)
            
            podcast_folder = os.path.join(args.output_dir, clean_podcast_name)
            filename = f'{clean_episode_title}.m4a'
            
            os.makedirs(podcast_folder, exist_ok=True)
            print(f'创建播客文件夹: {podcast_folder}')
            
            audio_path = download_file(audio_url, podcast_folder, filename)
            
            # 下载完成后，根据参数决定是否转写
            if args.transcribe:
                print('\n开始转写...')
                transcribe_audio(
                    audio_path,
                    model_size=args.model_size,
                    language='zh',
                    device=args.device,
                    compute_type=args.compute_type,
                    output_formats=args.output_formats,
                    output_dir=podcast_folder
                )
                print('✅ 下载并转写完成')
            else:
                print('✅ 下载完成')
        except Exception as e:
            print(f'❌ 错误: {e}')
            exit(1)
    
    elif args.command == 'transcribe':
        try:
            # 仅负责转写
            transcribe_audio(
                args.audio_path,
                model_size=args.model_size,
                language=args.language,
                device=args.device,
                compute_type=args.compute_type,
                output_formats=args.output_formats,
                output_dir=args.output_dir,
                word_timestamps=not args.no_word_timestamps,
                vad_filter=not args.no_vad_filter
            )
            print('✅ 转写完成')
        except Exception as e:
            print(f'❌ 错误: {e}')
            exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
