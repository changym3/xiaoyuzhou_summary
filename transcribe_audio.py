#!/usr/bin/env python3
import argparse
import os
import json
from faster_whisper import WhisperModel


def transcribe_audio(audio_path, model_size='small', language='zh', device='cpu', compute_type='int8',
                     output_formats=['txt', 'srt', 'json', 'md'], output_dir=None, word_timestamps=True, vad_filter=True, override=False):
    """
    使用 faster-whisper 转写音频文件
    
    Args:
        audio_path: 音频文件路径
        model_size: 模型大小 (tiny, base, small, medium, large-v2, large-v3)
        language: 语言代码 (zh, en, etc.)
        device: 计算设备 (cpu, cuda, auto)
        compute_type: 计算类型 (int8, float16, etc.)
        output_formats: 输出格式列表 (txt, srt, json, md)
        output_dir: 输出目录 (默认同音频目录
        word_timestamps: 是否输出词级时间戳
        vad_filter: 是否使用 VAD 过滤静音
        override: 是否覆盖已存在的文件
    
    Returns:
        list: 输出文件路径列表
    """
    if output_dir is None:
        output_dir = os.path.dirname(audio_path)
    
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    # 检查是否需要跳过
    txt_path = os.path.join(output_dir, f'{base_name}.txt')
    if os.path.exists(txt_path) and not override:
        print(f'✅ 转写文件已存在，跳过转写: {txt_path}')
        return [os.path.join(output_dir, f'{base_name}.{ext}') for ext in output_formats if os.path.exists(os.path.join(output_dir, f'{base_name}.{ext}'))
    
    print(f'正在加载模型: {model_size}')
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    
    print(f'正在转写: {audio_path}')
    
    vad_params = dict(min_silence_duration_ms=500) if vad_filter else None
    
    segments_generator, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=3,
        temperature=0.0,
        word_timestamps=word_timestamps,
        vad_filter=vad_filter,
        vad_parameters=vad_params
    )
    
    # 获取音频总时长
    total_duration = info.duration if hasattr(info, 'duration') else None
    
    # 收集所有 segments 并显示进度
    segments = []
    print('正在处理音频...', end='', flush=True)
    for i, segment in enumerate(segments_generator, 1):
        segments.append(segment)
        
        # 显示进度
        if total_duration:
            progress = min(segment.end / total_duration, 1.0)
            percent = progress * 100
            print(f'\r处理中... {percent:.1f}%', end='', flush=True)
        else:
            if i % 10 == 0:
                print(f'\r已处理 {i} 个片段...', end='', flush=True)
    
    if total_duration:
        print(f'\r处理完成！100.0%')
    else:
        print(f'\r处理完成！共 {len(segments)} 个片段')
    
    print(f'检测到语言: {info.language} (置信度: {info.language_probability:.2f})')
    
    output_files = []
    
    # 输出文本
    if 'txt' in output_formats:
        txt_path = os.path.join(output_dir, f'{base_name}.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            for segment in segments:
                f.write(segment.text.strip() + '\n')
        output_files.append(txt_path)
        print(f'已保存: {txt_path}')
    
    # 输出 Markdown
    if 'md' in output_formats:
        md_path = os.path.join(output_dir, f'{base_name}.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f'# {base_name}\n\n')
            f.write(f'**音频文件**: {os.path.basename(audio_path)}\n\n')
            f.write(f'**转写语言**: {info.language}\n\n')
            f.write(f'**置信度**: {info.language_probability:.2%}\n\n')
            f.write('---\n\n')
            for i, segment in enumerate(segments, 1):
                total_seconds = segment.start
                hours = int(total_seconds // 3600)
                minutes = int((total_seconds % 3600) // 60)
                seconds = int(total_seconds % 60)
                start_time = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                f.write(f'### [{start_time}]\n\n{segment.text.strip()}\n\n')
        output_files.append(md_path)
        print(f'已保存: {md_path}')
    
    # 输出 SRT
    if 'srt' in output_formats:
        srt_path = os.path.join(output_dir, f'{base_name}.srt')
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start_h = int(segment.start // 3600)
                start_m = int((segment.start % 3600) // 60)
                start_s = int(segment.start % 60)
                start_ms = int((segment.start % 1) * 1000)
                
                end_h = int(segment.end // 3600)
                end_m = int((segment.end % 3600) // 60)
                end_s = int(segment.end % 60)
                end_ms = int((segment.end % 1) * 1000)
                
                f.write(f'{i}\n')
                f.write(f'{start_h:02d}:{start_m:02d}:{start_s:02d},{start_ms:03d} --> ')
                f.write(f'{end_h:02d}:{end_m:02d}:{end_s:02d},{end_ms:03d}\n')
                f.write(segment.text.strip() + '\n\n')
        output_files.append(srt_path)
        print(f'已保存: {srt_path}')
    
    # 输出 JSON
    if 'json' in output_formats:
        json_path = os.path.join(output_dir, f'{base_name}.json')
        json_data = {
            'info': {
                'language': info.language,
                'language_probability': info.language_probability,
                'duration': info.duration if hasattr(info, 'duration') else None
            },
            'segments': []
        }
        
        for segment in segments:
            segment_dict = {
                'start': segment.start,
                'end': segment.end,
                'text': segment.text.strip(),
                'words': []
            }
            if hasattr(segment, 'words') and segment.words:
                for word in segment.words:
                    segment_dict['words'].append({
                        'word': word.word,
                        'start': word.start,
                        'end': word.end,
                        'probability': word.probability if hasattr(word, 'probability') else None
                    })
            json_data['segments'].append(segment_dict)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        output_files.append(json_path)
        print(f'已保存: {json_path}')
    
    return output_files


def main():
    parser = argparse.ArgumentParser(description='使用 faster-whisper 转写音频文件')
    parser.add_argument('audio_path', help='音频文件路径')
    parser.add_argument('--model-size', default='small', choices=['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3'],
                        help='模型大小 (默认：small)')
    parser.add_argument('--language', default='zh', help='语言代码 (默认：zh)')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda', 'auto'],
                        help='计算设备 (默认：cpu)')
    parser.add_argument('--compute-type', default='int8', choices=['int8', 'int8_float16', 'float16', 'float32'],
                        help='计算类型 (默认：int8)')
    parser.add_argument('--output-formats', nargs='+', default=['txt', 'srt', 'json', 'md'],
                        choices=['txt', 'srt', 'json', 'md'],
                        help='输出格式 (默认：txt srt json md)')
    parser.add_argument('--output-dir', help='输出目录 (默认同音频目录)')
    parser.add_argument('--no-word-timestamps', action='store_true', help='不输出词级时间戳')
    parser.add_argument('--no-vad-filter', action='store_true', help='不使用 VAD 过滤静音')
    parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    args = parser.parse_args()
    
    try:
        transcribe_audio(
            args.audio_path,
            model_size=args.model_size,
            language=args.language,
            device=args.device,
            compute_type=args.compute_type,
            output_formats=args.output_formats,
            output_dir=args.output_dir,
            word_timestamps=not args.no_word_timestamps,
            vad_filter=not args.no_vad_filter,
            override=args.override
        )
        print('✅ 转写完成')
    except Exception as e:
        print(f'❌ 错误: {e}')
        exit(1)


if __name__ == '__main__':
    main()
