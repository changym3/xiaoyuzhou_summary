#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI


def load_env():
    # 尝试从脚本所在目录加载 .env
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    load_dotenv(env_path)
    
    api_key = os.getenv('LLM_API_KEY')
    base_url = os.getenv('LLM_BASE_URL', 'https://api.deepseek.com')
    model = os.getenv('LLM_MODEL', 'deepseek-chat')
    
    # 调试信息
    if not api_key:
        print(f'⚠️  尝试加载 .env 文件: {env_path}')
        if os.path.exists(env_path):
            print('⚠️  .env 文件存在，但 LLM_API_KEY 为空或未设置')
        else:
            print(f'⚠️  .env 文件不存在: {env_path}')
    
    return api_key, base_url, model


def summarize_text(text, api_key, base_url, model, prompt=None, max_tokens=4000):
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    if prompt is None:
        prompt = """请为以下对话/文本生成详细的逻辑摘要，按以下结构组织：

【对话概述】
详细描述本次对话的主题、参与人员和整体脉络

【对话逻辑脉络】
按时间顺序记录对话的演进过程：
1. 开篇话题（如何引入主题）
2. 主要讨论点（按顺序列出每个核心话题）
   - 话题1：[内容] + [关键观点/论据]
   - 话题2：[内容] + [关键观点/论据]
   - ...
3. 话题转折（如有观点变化或新方向引入）
4. 结论/收尾

【关键信息摘录】
- 重要数据/事实
- 核心观点/主张
- 行动建议/下一步计划

【逻辑关系图】
用简洁的方式描述各话题之间的关联（如：递进、并列、转折等）

请用中文回答，确保：
1. 严格保持对话的时间顺序
2. 准确记录每个文本片段的逻辑贡献
3. 突出观点之间的联系和演进
4. 如果有明确的说话人，请注明发言者"""
    
    messages = [
        {"role": "system", "content": "你是一个专业的文本总结助手。"},
        {"role": "user", "content": f"{prompt}\n\n以下是需要总结的文本：\n\n{text}"}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content


def summarize_file(txt_path, output_path=None, api_key=None, base_url=None, model=None, prompt=None, max_tokens=4000, override=False):
    if api_key is None or base_url is None or model is None:
        api_key, base_url, model = load_env()
    
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(txt_path))[0]
        output_dir = os.path.dirname(txt_path)
        output_path = os.path.join(output_dir, f'{base_name}_summary.md')
    
    # 检查是否需要跳过
    if os.path.exists(output_path) and not override:
        print(f'✅ 总结文件已存在，跳过总结: {output_path}')
        return output_path, None
    
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f'正在总结: {txt_path}')
    summary = summarize_text(text, api_key, base_url, model, prompt, max_tokens)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f'已保存总结: {output_path}')
    return output_path, summary


def main():
    parser = argparse.ArgumentParser(description='使用大模型API对文本进行总结')
    parser.add_argument('txt_path', help='文本文件路径')
    parser.add_argument('--output', help='输出文件路径 (默认: 原文件名_summary.txt)')
    parser.add_argument('--api-key', help='大模型API密钥 (优先使用环境变量 LLM_API_KEY)')
    parser.add_argument('--base-url', help='大模型API基础URL (优先使用环境变量 LLM_BASE_URL, 默认: https://api.deepseek.com)')
    parser.add_argument('--model', help='大模型名称 (优先使用环境变量 LLM_MODEL, 默认: deepseek-chat)')
    parser.add_argument('--prompt', help='自定义总结提示词')
    parser.add_argument('--max-tokens', type=int, default=4000, help='最大输出token数 (默认: 4000)')
    parser.add_argument('--override', action='store_true', help='覆盖已存在的文件')
    
    args = parser.parse_args()
    
    # 确保先加载 .env 文件
    if not args.api_key:
        load_env()
    
    api_key = args.api_key or os.getenv('LLM_API_KEY')
    base_url = args.base_url or os.getenv('LLM_BASE_URL', 'https://api.deepseek.com')
    model = args.model or os.getenv('LLM_MODEL', 'deepseek-chat')
    
    if not api_key:
        print('❌ 错误: 未设置 LLM_API_KEY 环境变量或 --api-key 参数')
        exit(1)
    
    try:
        summarize_file(
            args.txt_path,
            output_path=args.output,
            api_key=api_key,
            base_url=base_url,
            model=model,
            prompt=args.prompt,
            max_tokens=args.max_tokens,
            override=args.override
        )
        print('✅ 总结完成')
    except Exception as e:
        print(f'❌ 错误: {e}')
        exit(1)


if __name__ == '__main__':
    main()
