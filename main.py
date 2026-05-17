#!/usr/bin/env python3
import argparse
import os
from download_from_url import get_episode_info, download_file, sanitize_filename
from transcribe_audio import transcribe_audio
from summarize_text import summarize_file, load_env


def download_podcast(url, output_dir='outputs', override=False):
    """下载播客音频"""
    audio_url, podcast_name, episode_title = get_episode_info(url)
    print(f'找到播客节目: {podcast_name}')
    print(f'找到单集标题: {episode_title}')
    print(f'找到音频 URL: {audio_url}')
    
    clean_podcast_name = sanitize_filename(podcast_name)
    clean_episode_title = sanitize_filename(episode_title)
    
    podcast_folder = os.path.join(output_dir, clean_podcast_name)
    filename = f'{clean_episode_title}.m4a'
    audio_path = os.path.join(podcast_folder, filename)
    
    os.makedirs(podcast_folder, exist_ok=True)
    print(f'创建播客文件夹: {podcast_folder}')
    
    audio_path = download_file(audio_url, podcast_folder, filename, override=override)
    return audio_path, podcast_folder, clean_episode_title


def transcribe_audio_file(audio_path, model_size='small', device='cpu', compute_type='int8', 
                          output_formats=['txt', 'srt', 'json'], output_dir=None, 
                          word_timestamps=True, vad_filter=True, override=False):
    """转录音频文件"""
    if output_dir is None:
        output_dir = os.path.dirname(audio_path)
    
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    transcribe_audio(
        audio_path,
        model_size=model_size,
        language='zh',
        device=device,
        compute_type=compute_type,
        output_formats=output_formats,
        output_dir=output_dir,
        word_timestamps=word_timestamps,
        vad_filter=vad_filter,
        override=override
    )
    return os.path.join(output_dir, f'{base_name}.txt')


def summarize_text_file(txt_path, output_path=None, api_key=None, base_url=None, 
                        model=None, prompt=None, max_tokens=4000, override=False):
    """总结文本文件"""
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(txt_path))[0]
        output_dir = os.path.dirname(txt_path)
        output_path = os.path.join(output_dir, f'{base_name}_summary.md')
    
    if api_key is None or base_url is None or model is None:
        api_key_env, base_url_env, model_env = load_env()
        api_key = api_key or api_key_env
        base_url = base_url or base_url_env
        model = model or model_env
    
    if not api_key:
        print('⚠️ 未设置 LLM_API_KEY，跳过总结')
        return None
    
    summarize_file(
        txt_path,
        output_path=output_path,
        api_key=api_key,
        base_url=base_url,
        model=model,
        prompt=prompt,
        max_tokens=max_tokens,
        override=override
    )
    return output_path


def main():
    parser = argparse.ArgumentParser(description='ASR 项目：播客下载、语音转写、文本总结')
    subparsers = parser.add_subparsers(title='子命令', dest='command', help='可用命令')
    
    # 下载子命令
    download_parser = subparsers.add_parser('download', help='下载播客音频')
    download_parser.add_argument('url', help='小宇宙播客单集页面 URL')
    download_parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录 (默认: outputs)')
    download_parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    # 转写子命令
    transcribe_parser = subparsers.add_parser('transcribe', help='转写音频文件')
    transcribe_parser.add_argument('audio_path', help='音频文件路径')
    transcribe_parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                                  help='模型大小 (默认: small)')
    transcribe_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                                  help='计算设备 (默认: cpu)')
    transcribe_parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                                  help='计算类型 (默认: int8)')
    transcribe_parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json', 'md'],
                                  choices=['txt', 'srt', 'json', 'md'],
                                  help='输出格式 (默认: txt srt json md)')
    transcribe_parser.add_argument('--output-dir', help='输出目录 (默认同音频目录)')
    transcribe_parser.add_argument('--no-word-timestamps', action='store_true', help='不输出词级时间戳')
    transcribe_parser.add_argument('--no-vad-filter', action='store_true', help='不使用 VAD 过滤静音')
    transcribe_parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    # 总结子命令
    summarize_parser = subparsers.add_parser('summarize', help='总结文本文件')
    summarize_parser.add_argument('txt_path', help='文本文件路径')
    summarize_parser.add_argument('--output', help='输出文件路径 (默认: 原文件名_summary.md)')
    summarize_parser.add_argument('--api-key', help='大模型 API 密钥 (优先使用环境变量 LLM_API_KEY)')
    summarize_parser.add_argument('--base-url', help='大模型 API 基础 URL (优先使用环境变量 LLM_BASE_URL)')
    summarize_parser.add_argument('--model', help='大模型名称 (优先使用环境变量 LLM_MODEL)')
    summarize_parser.add_argument('--prompt', help='自定义总结提示词')
    summarize_parser.add_argument('--max-tokens', type=int, default=4000, help='最大输出 token 数 (默认: 4000)')
    summarize_parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    # 流水线子命令 - 一站式处理
    pipeline_parser = subparsers.add_parser('pipeline', help='一站式处理：下载 -> 转写 -> 总结')
    pipeline_parser.add_argument('url', help='小宇宙播客单集页面 URL')
    pipeline_parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录 (默认: outputs)')
    pipeline_parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                               help='模型大小 (默认: small)')
    pipeline_parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                               help='计算设备 (默认: cpu)')
    pipeline_parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                               help='计算类型 (默认: int8)')
    pipeline_parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json', 'md'],
                               choices=['txt', 'srt', 'json', 'md'],
                               help='转写输出格式 (默认: txt srt json md)')
    pipeline_parser.add_argument('--no-word-timestamps', action='store_true', help='不输出词级时间戳')
    pipeline_parser.add_argument('--no-vad-filter', action='store_true', help='不使用 VAD 过滤静音')
    pipeline_parser.add_argument('--summarize-prompt', help='自定义总结提示词')
    pipeline_parser.add_argument('--summarize-max-tokens', type=int, default=4000, help='总结最大输出 token 数 (默认: 4000)')
    pipeline_parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'download':
            download_podcast(args.url, args.output_dir, override=args.override)
            print('✅ 下载完成')
        
        elif args.command == 'transcribe':
            transcribe_audio_file(
                args.audio_path,
                model_size=args.model_size,
                device=args.device,
                compute_type=args.compute_type,
                output_formats=args.output_formats,
                output_dir=args.output_dir,
                word_timestamps=not args.no_word_timestamps,
                vad_filter=not args.no_vad_filter,
                override=args.override
            )
            print('✅ 转写完成')
        
        elif args.command == 'summarize':
            summarize_text_file(
                args.txt_path,
                output_path=args.output,
                api_key=args.api_key,
                base_url=args.base_url,
                model=args.model,
                prompt=args.prompt,
                max_tokens=args.max_tokens,
                override=args.override
            )
            print('✅ 总结完成')
        
        elif args.command == 'pipeline':
            print('=' * 50)
            print('开始流水线处理：下载 -> 转写 -> 总结')
            print('=' * 50)
            
            # 1. 下载
            print('\n[步骤 1/3] 下载播客...')
            audio_path, podcast_folder, _ = download_podcast(args.url, args.output_dir, override=args.override)
            
            # 2. 转写
            print('\n[步骤 2/3] 转写音频...')
            txt_path = transcribe_audio_file(
                audio_path,
                model_size=args.model_size,
                device=args.device,
                compute_type=args.compute_type,
                output_formats=args.output_formats,
                output_dir=podcast_folder,
                word_timestamps=not args.no_word_timestamps,
                vad_filter=not args.no_vad_filter,
                override=args.override
            )
            
            # 3. 总结
            print('\n[步骤 3/3] 总结文本...')
            summarize_text_file(
                txt_path,
                prompt=args.summarize_prompt,
                max_tokens=args.summarize_max_tokens,
                override=args.override
            )
            
            print('\n' + '=' * 50)
            print('✅ 流水线处理完成！')
            print('=' * 50)
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f'❌ 错误: {e}')
        exit(1)


if __name__ == '__main__':
    main()
