#!/usr/bin/env python3
import argparse
import os
from download_from_url import get_episode_info, download_file, sanitize_filename
from transcribe_audio import transcribe_audio
from summarize_text import summarize_file, load_env


def main():
    parser = argparse.ArgumentParser(description='ASR 项目：播客下载与语音转写（统一调度入口')
    subparsers = parser.add_subparsers(title='子命令', dest='command', help='可用命令')
    
    # 下载子命令
    download_parser = subparsers.add_parser('download', help='下载播客音频（仅下载')
    download_parser.add_argument('url', help='小宇宙播客单集页面 URL')
    download_parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录（默认：outputs）')
    download_parser.add_argument('--transcribe', action='store_true', help='下载后自动转写')
    download_parser.add_argument('--summarize', action='store_true', help='转写后自动总结（需配合 --transcribe 使用）')
    download_parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                               help='转写模型大小（默认：small）')
    download_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                               help='计算设备（默认：cpu）')
    download_parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                               help='计算类型（默认：int8）')
    download_parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json'],
                               choices=['txt', 'srt', 'json'],
                               help='转写输出格式（默认：txt srt json）')
    download_parser.add_argument('--summarize-prompt', help='自定义总结提示词')
    
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
    transcribe_parser.add_argument('--summarize', action='store_true', help='转写后自动总结')
    transcribe_parser.add_argument('--summarize-prompt', help='自定义总结提示词')
    
    # 总结子命令
    summarize_parser = subparsers.add_parser('summarize', help='总结文本文件')
    summarize_parser.add_argument('txt_path', help='文本文件路径')
    summarize_parser.add_argument('--output', help='输出文件路径 (默认: 原文件名_summary.txt)')
    summarize_parser.add_argument('--api-key', help='大模型API密钥 (优先使用环境变量 LLM_API_KEY)')
    summarize_parser.add_argument('--base-url', help='大模型API基础URL (优先使用环境变量 LLM_BASE_URL)')
    summarize_parser.add_argument('--model', help='大模型名称 (优先使用环境变量 LLM_MODEL)')
    summarize_parser.add_argument('--prompt', help='自定义总结提示词')
    
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
            
            # 检查是否已下载
            audio_path = os.path.join(podcast_folder, filename)
            if os.path.exists(audio_path):
                print(f'✅ 音频文件已存在，跳过下载: {audio_path}')
            else:
                audio_path = download_file(audio_url, podcast_folder, filename)
            
            # 下载完成后，根据参数决定是否转写
            if args.transcribe:
                # 检查是否已转写
                base_name = os.path.splitext(os.path.basename(audio_path))[0]
                txt_path = os.path.join(podcast_folder, f'{base_name}.txt')
                
                if os.path.exists(txt_path):
                    print(f'✅ 转写文件已存在，跳过转写: {txt_path}')
                else:
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
                
                # 检查是否需要总结
                if args.summarize:
                    summary_path = os.path.join(podcast_folder, f'{base_name}_summary.txt')
                    if os.path.exists(summary_path):
                        print(f'✅ 总结文件已存在，跳过总结: {summary_path}')
                    else:
                        print('\n开始总结...')
                        api_key, base_url, model = load_env()
                        if api_key:
                            summarize_file(
                                txt_path,
                                api_key=api_key,
                                base_url=base_url,
                                model=model,
                                prompt=args.summarize_prompt
                            )
                        else:
                            print('⚠️  未设置 LLM_API_KEY，跳过总结')
                print('✅ 全部完成')
            else:
                print('✅ 下载完成')
        except Exception as e:
            print(f'❌ 错误: {e}')
            exit(1)
    
    elif args.command == 'transcribe':
        try:
            audio_path = args.audio_path
            output_dir = args.output_dir or os.path.dirname(audio_path)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            txt_path = os.path.join(output_dir, f'{base_name}.txt')
            
            # 检查是否已转写
            if os.path.exists(txt_path):
                print(f'✅ 转写文件已存在，跳过转写: {txt_path}')
            else:
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
            
            # 检查是否需要总结
            if args.summarize:
                summary_path = os.path.join(output_dir, f'{base_name}_summary.txt')
                if os.path.exists(summary_path):
                    print(f'✅ 总结文件已存在，跳过总结: {summary_path}')
                else:
                    print('\n开始总结...')
                    api_key, base_url, model = load_env()
                    if api_key:
                        summarize_file(
                            txt_path,
                            api_key=api_key,
                            base_url=base_url,
                            model=model,
                            prompt=args.summarize_prompt
                        )
                    else:
                        print('⚠️  未设置 LLM_API_KEY，跳过总结')
            print('✅ 转写完成')
        except Exception as e:
            print(f'❌ 错误: {e}')
            exit(1)
    
    elif args.command == 'summarize':
        try:
            # 检查输出文件是否存在
            output_path = args.output
            if output_path is None:
                base_name = os.path.splitext(os.path.basename(args.txt_path))[0]
                output_dir = os.path.dirname(args.txt_path)
                output_path = os.path.join(output_dir, f'{base_name}_summary.txt')
            
            if os.path.exists(output_path):
                print(f'✅ 总结文件已存在，跳过总结: {output_path}')
            else:
                # 获取配置
                api_key = args.api_key
                base_url = args.base_url
                model = args.model
                
                if not api_key:
                    api_key, base_url_env, model_env = load_env()
                    base_url = base_url or base_url_env
                    model = model or model_env
                
                if not api_key:
                    print('❌ 错误: 未设置 LLM_API_KEY 环境变量或 --api-key 参数')
                    exit(1)
                
                summarize_file(
                    args.txt_path,
                    output_path=args.output,
                    api_key=api_key,
                    base_url=base_url,
                    model=model,
                    prompt=args.prompt
                )
            print('✅ 总结完成')
        except Exception as e:
            print(f'❌ 错误: {e}')
            exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
