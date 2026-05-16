# 文本总结功能问答

## Q: 这个功能是做什么的？
A: 该功能可以对转写后的文本或任何文本文件使用大模型 API 进行智能总结，提取关键信息和核心要点。

## Q: 需要配置哪些环境变量？
A: 需要配置以下环境变量（可通过 .env 文件设置）：
- LLM_API_KEY：大模型 API 密钥（必需）
- LLM_BASE_URL：API 基础 URL（默认 https://api.openai.com/v1）
- LLM_MODEL：模型名称（默认 gpt-3.5-turbo）

## Q: 如何配置环境变量？
A: 步骤如下：
1. 复制 .env.example 为 .env：`cp .env.example .env`
2. 用文本编辑器打开 .env 文件
3. 填入你的真实 API 配置信息
4. 保存文件

## Q: 如何直接总结一个文本文件？
A: 使用 summarize_text.py 脚本：
```bash
uv run python summarize_text.py path/to/your/text.txt
```

## Q: 如何在转写音频时自动生成总结？
A: 在 transcribe_audio.py 命令中添加 --summarize 参数：
```bash
uv run python transcribe_audio.py --summarize path/to/audio.m4a
```

## Q: 可以使用自定义提示词吗？
A: 可以！使用 --summarize-prompt 参数（或 --prompt 参数）：
```bash
# 独立使用时
uv run python summarize_text.py --prompt "请用 bullet points 格式总结" text.txt

# 转写集成时
uv run python transcribe_audio.py --summarize --summarize-prompt "请用 bullet points 格式总结" audio.m4a
```

## Q: 支持哪些大模型？
A: 支持所有 OpenAI 兼容的 API 接口，包括：
- Deepseek（已默认配置，推荐使用）
- OpenAI 官方模型（GPT-3.5, GPT-4 等）
- Claude API（需要配置合适的 base_url）
- 国内模型如通义千问、智谱、文心一言等（需要配置对应 base_url 和模型名称）

## Q: 如何配置 Deepseek 需要什么？
A: 项目已默认配置 Deepseek，你只需：
1. 复制 .env.example 为 .env
2. 在 .env 中填入你的 Deepseek API Key
3. 无需修改其他配置（默认已设置好：
   - LLM_BASE_URL=https://api.deepseek.com
   - LLM_MODEL=deepseek-chat

## Q: API 密钥安全吗？
A: 是的，我们采用以下安全措施：
1. 密钥通过环境变量管理，不硬编码在代码中
2. .env 文件已被添加到 .gitignore，不会被提交到版本控制
3. 你也可以通过命令行参数临时传入密钥（不推荐用于生产环境）

## Q: 总结结果保存在哪里？
A: 总结结果会自动保存为 `原文件名_summary.txt`，与原文件在同一目录下。

## Q: 如何安装所需的依赖？
A: 使用 uv 同步依赖：
```bash
uv sync
```
