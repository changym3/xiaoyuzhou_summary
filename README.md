# ASR Project - 播客下载、语音转写与智能总结工具

一个用于从小宇宙（xiaoyuzhoufm.com）下载播客、使用 faster-whisper 进行自动语音转写，并通过大模型 API 进行文本总结的 Python 工具。

## 功能特性

- 🎧 **播客下载**：从小宇宙播客页面下载 m4a 音频文件
- 📝 **语音转写**：使用 faster-whisper 进行本地语音转写（无 token 限制）
- 🤖 **智能总结**：通过大模型 API（支持 Deepseek、OpenAI 等）自动总结转写内容
- 📂 **智能组织**：按播客名称自动创建文件夹整理文件
- 📄 **多格式输出**：转写支持 TXT、SRT、JSON、Markdown 四种格式，总结输出为 Markdown
- ⚡ **灵活配置**：支持多种模型大小和转写参数调整
- 🛡️ **智能跳过**：自动检测并跳过已完成的下载、转写或总结
- 🏗️ **清晰架构**：职责分离，各模块独立可复用

## 安装

### 环境要求
- Python 3.13+
- macOS / Linux / Windows
- 足够的磁盘空间（模型下载 + 音频存储）
- 大模型 API Key（如 Deepseek、OpenAI 等，用于总结功能）

### 安装步骤

1. 克隆或下载项目：
```bash
cd asr_project
```

2. 使用 uv 安装依赖：
```bash
uv sync
```

3. 配置大模型 API（可选，仅使用总结功能时需要）：
```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 默认已配置好 Deepseek 的 base URL 和模型
```

## 架构设计

### 职责分离
每个模块单一职责，互不依赖：
- **download_from_url.py**：只负责下载播客音频
- **transcribe_audio.py**：只负责音频转写（无 token 限制）
- **summarize_text.py**：只负责文本总结
- **main.py**：统一调度入口，支持独立使用和流水线处理

## 使用方法

### 方式一：使用 main.py（推荐）

#### 1. 独立使用各功能

```bash
# 只下载播客
uv run python main.py download <小宇宙播客URL>

# 只转写音频
uv run python main.py transcribe <音频文件路径>

# 只总结文本
uv run python main.py summarize <文本文件路径>
```

#### 2. 流水线处理（一站式）

```bash
# 下载 -> 转写 -> 总结，一键完成
uv run python main.py pipeline <小宇宙播客URL>
```

#### 3. 参数调整

```bash
# 指定模型大小
uv run python main.py transcribe <音频文件> --model-size medium

# 自定义输出目录
uv run python main.py download <URL> --output-dir ./my_podcasts

# 自定义总结提示词和长度
uv run python main.py summarize <文本文件> --prompt "请用 bullet points 总结" --max-tokens 8000

# 流水线时指定参数
uv run python main.py pipeline <URL> --model-size large-v3 --summarize-max-tokens 6000

# 强制覆盖已存在文件（不会跳过）
uv run python main.py download <URL> --override
uv run python main.py transcribe <音频文件> --override
uv run python main.py summarize <文本文件> --override
uv run python main.py pipeline <URL> --override
```

#### 4. 使用示例

```bash
# 示例：处理一期播客（完整流程）
uv run python main.py pipeline https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1

# 示例：强制重新处理（覆盖已存在文件）
uv run python main.py pipeline https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1 --override
```

### 方式二：直接使用独立模块

各模块也可以独立运行：

```bash
# 仅使用下载模块
uv run python download_from_url.py <URL>

# 仅使用转写模块
uv run python transcribe_audio.py <音频文件>

# 仅使用总结模块
uv run python summarize_text.py <文本文件>
```

## 输出格式

### 转写输出（四种格式）
1. **TXT**：纯文本，易读性好
2. **Markdown (.md)**：结构化格式，带时间戳标题，便于阅读
3. **SRT**：字幕格式，带时间戳
4. **JSON**：完整数据，含词级时间戳和置信度

### 总结输出
- **Markdown (.md)**：结构化的 Markdown 格式，便于阅读和分享

## 模型对比

| 模型 | 大小 | 速度 | 准确率 | 推荐场景 |
|------|------|------|--------|----------|
| tiny | ~150MB | 🔥🔥🔥🔥🔥 | ⭐⭐ | 快速预览 |
| base | ~300MB | 🔥🔥🔥🔥 | ⭐⭐⭐ | 日常使用 |
| small | ~500MB | 🔥🔥🔥 | ⭐⭐⭐⭐ | **默认推荐** |
| medium | ~1.5GB | 🔥🔥 | ⭐⭐⭐⭐⭐ | 高质量需求 |
| large-v3 | ~3GB | 🔥 | ⭐⭐⭐⭐⭐+ | 极致质量 |

## macOS 性能优化

faster-whisper 目前不支持 Apple MPS (Metal) 加速，默认使用 CPU：

- 默认配置已优化为 `small` 模型，平衡速度与准确率
- 如需要更快速度，使用 `--model-size base` 或 `tiny`
- 如需要更高质量，使用 `--model-size medium`

## 项目结构

```
asr_project/
├── main.py              # 统一调度入口
├── download_from_url.py # 下载模块（独立）
├── transcribe_audio.py  # 转写模块（独立）
├── summarize_text.py    # 总结模块（独立）
├── pyproject.toml       # 项目配置
├── uv.lock              # 依赖锁定
├── .env.example         # 环境变量配置模板
├── Task/                # 任务记录
├── QA/                  # 问答文档
├── tests/               # 测试文件
└── outputs/             # 默认输出目录（git 已忽略）
```

## 配置说明

### 转写配置
- 默认输出目录：`./outputs`
- 默认模型：`small`
- 默认语言：`zh`（中文）
- VAD 过滤：默认开启（过滤静音片段）
- 词级时间戳：默认开启
- **无 token 限制**：完整转录任意长度的音频

### 总结配置
通过 `.env` 文件配置：
- `LLM_API_KEY`：大模型 API 密钥（必需）
- `LLM_BASE_URL`：API 基础 URL（默认 Deepseek）
- `LLM_MODEL`：模型名称（默认 deepseek-chat）

支持的 API：Deepseek、OpenAI 及其他 OpenAI 兼容接口

## 常见问题

### Q: 首次运行很慢？
A: 首次运行会自动下载模型到缓存目录，后续会很快。

### Q: 如何更换模型？
A: 使用 `--model-size` 参数即可，程序会自动下载新模型。

### Q: 支持哪些音频格式？
A: 支持 m4a、mp3、wav、flac 等常见格式。

### Q: macOS 上能否更快？
A: 当前 faster-whisper 不支持 MPS，如需极致性能可考虑 whisper.cpp 或 MLX 框架。

### Q: 如何使用总结功能？
A: 需要先配置 `.env` 文件中的 `LLM_API_KEY`。

### Q: 支持哪些大模型？
A: 支持所有 OpenAI 兼容接口，包括 Deepseek（默认）、OpenAI 等。

### Q: 程序会重复下载/转写/总结吗？
A: 不会！程序会自动检测文件是否存在，如果存在会跳过对应步骤。

### Q: 如何强制重新生成？
A: 使用 `--override` 参数即可强制覆盖已存在的文件并重新执行，例如：
```bash
uv run python main.py pipeline <URL> --override
```
或者手动删除对应的输出文件也可以。

### Q: 转录有 token 限制吗？
A: **没有！** 转录功能完全没有 token 限制，可以完整处理任意长度的音频。只有总结功能有 max_tokens 参数（因为 LLM API 有上下文限制）。

## 技术栈

- [faster-whisper](https://github.com/guillaumekln/faster-whisper)：高效的 Whisper 实现
- [requests](https://requests.readthedocs.io/)：HTTP 请求库
- [uv](https://astral.sh/uv)：现代 Python 包管理和运行工具
- [openai](https://pypi.org/project/openai/)：OpenAI 兼容 API 客户端
- [python-dotenv](https://pypi.org/project/python-dotenv/)：环境变量管理

## 许可证

本项目仅供学习和个人使用。请遵守播客内容的版权和使用条款。
