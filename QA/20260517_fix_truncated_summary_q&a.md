# 修复总结文本被截断问题问答

## Q: 为什么总结文本会被截断？
A: 因为代码中有一个 `max_tokens=1000` 的限制，对于我们新的详细结构化提示词来说，这个限制太小了。

## Q: 这个参数在哪里设置的？
A: 原来在 `summarize_text.py:52` 硬编码为 1000，现在已经改为可配置参数。

## Q: 默认值是多少？
A: 默认值已提升到 4000 tokens，足够生成完整的结构化总结。

## Q: 可以自定义输出长度吗？
A: 可以！使用 `--max-tokens` 参数：

```bash
# 总结文本时
uv run python summarize_text.py --max-tokens 8000 text.txt

# 转写音频时
uv run python transcribe_audio.py --summarize --summarize-max-tokens 6000 audio.m4a

# 使用 main.py
uv run python main.py summarize --max-tokens 8000 text.txt
```

## Q: max_tokens 设置多大合适？
A: 
- 简短总结：1000-2000
- 普通总结：2000-4000 (默认)
- 详细总结：4000-8000
- 超长总结：8000+

注意：不同的模型有不同的上下文窗口限制，请根据你使用的模型调整。

## Q: 修改了哪些文件？
A:
- `summarize_text.py` - 核心逻辑
- `transcribe_audio.py` - 转写集成
- `main.py` - 统一调度入口

## Q: 会影响现有功能吗？
A: 不会！默认值已经设置好了，现有代码可以继续正常使用，无需修改任何参数。

## Q: 任务记录在哪里？
A: 在 `Task/20260517_fix_truncated_summary.md`
