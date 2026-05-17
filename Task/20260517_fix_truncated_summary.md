# 修复总结文本被截断问题

## 问题描述
用户发现总结文本被截断，无法完整输出。

## 原因分析
在 `summarize_text.py:52` 中有一个 `max_tokens=1000` 的限制，对于我们新的详细结构化提示词来说，这个限制太小了。

## 解决方案
1. 将默认 `max_tokens` 从 1000 提升到 4000
2. 添加 `max_tokens` 参数支持，让用户可以灵活调整
3. 更新所有相关函数和命令行接口

## 修改文件
- `summarize_text.py`
  - `summarize_text()` 函数添加 `max_tokens` 参数
  - `summarize_file()` 函数添加 `max_tokens` 参数
  - `main()` 函数添加 `--max-tokens` 命令行参数
  - 默认值从 1000 改为 4000

- `transcribe_audio.py`
  - `transcribe_audio()` 函数添加 `summarize_max_tokens` 参数
  - `main()` 函数添加 `--summarize-max-tokens` 命令行参数

- `main.py`
  - `download` 子命令添加 `--summarize-max-tokens` 参数
  - `transcribe` 子命令添加 `--summarize-max-tokens` 参数
  - `summarize` 子命令添加 `--max-tokens` 参数

## 使用方法
```bash
# 使用默认值 (4000 tokens)
uv run python summarize_text.py text.txt

# 自定义输出长度
uv run python summarize_text.py --max-tokens 8000 text.txt

# 在转写时使用
uv run python transcribe_audio.py --summarize --summarize-max-tokens 6000 audio.m4a

# 使用 main.py
uv run python main.py summarize --max-tokens 8000 text.txt
```
