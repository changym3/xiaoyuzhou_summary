# ASR Project - 播客下载与语音转写工具

一个用于从小宇宙（xiaoyuzhoufm.com）下载播客并使用 faster-whisper 进行自动语音转写的 Python 工具。

## 功能特性

- 🎧 **播客下载**：从小宇宙播客页面下载 m4a 音频文件
- 📝 **语音转写**：使用 faster-whisper 进行本地语音转写
- 📂 **智能组织**：按播客名称自动创建文件夹整理文件
- 📄 **多格式输出**：支持 TXT、SRT、JSON 三种输出格式
- ⚡ **灵活配置**：支持多种模型大小和转写参数调整

## 安装

### 环境要求
- Python 3.13+
- macOS / Linux / Windows
- 足够的磁盘空间（模型下载 + 音频存储）

### 安装步骤

1. 克隆或下载项目：
```bash
cd asr_project
```

2. 使用 uv 安装依赖：
```bash
uv sync
```

## 使用方法

### 架构设计
- **职责分离**：每个模块单一职责
- **统一调度**：main.py 负责整体流程
- **模块独立**：download 和 transcribe 互不依赖

### 1. 仅下载播客（默认）

```bash
uv run python main.py download <小宇宙播客URL>
```

示例：
```bash
uv run python main.py download https://www.xiaoyuzhoufm.com/episode/xxx
```

### 2. 下载并自动转写

```bash
uv run python main.py download <URL> --transcribe
```

### 3. 仅转写已有音频文件

```bash
uv run python main.py transcribe <音频文件路径>
```

### 4. 调整转写参数

```bash
# 下载后自动转写，并指定参数
uv run python main.py download <URL> --transcribe --model-size tiny
uv run python main.py download <URL> --transcribe --model-size medium

# 独立转写音频文件
uv run python main.py transcribe <音频文件> --model-size large-v3

# 指定输出格式
uv run python main.py download <URL> --transcribe --output-formats txt json

# 自定义输出目录
uv run python main.py download <URL> --output-dir ./my_podcasts
```

### 使用说明

- `download_from_url.py`：**仅下载**的独立脚本
- `transcribe_audio.py`：**仅转写**的独立模块  
- `main.py`：**统一调度入口**，支持灵活组合下载和转写

### 直接使用独立模块

也可以直接调用独立模块：
```bash
# 仅使用下载模块
uv run python download_from_url.py <URL>

# 仅使用转写模块
uv run python transcribe_audio.py <音频文件>
```

## 输出格式

默认输出三种格式到同目录下：

1. **TXT**：纯文本，易读性好
2. **SRT**：字幕格式，带时间戳
3. **JSON**：完整数据，含词级时间戳和置信度

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
├── main.py              # 主程序入口
├── download_from_url.py # 下载模块
├── transcribe_audio.py  # 转写模块
├── pyproject.toml       # 项目配置
├── uv.lock              # 依赖锁定
├── Task/                # 任务记录
├── QA/                  # 问答文档
├── tests/               # 测试文件
└── outputs/             # 默认输出目录（git 已忽略）
```

## 配置说明

- 默认输出目录：`./outputs`
- 默认模型：`small`
- 默认语言：`zh`（中文）
- VAD 过滤：默认开启（过滤静音片段）
- 词级时间戳：默认开启

## 常见问题

### Q: 首次运行很慢？
A: 首次运行会自动下载模型到缓存目录，后续会很快。

### Q: 如何更换模型？
A: 使用 `--model-size` 参数即可，程序会自动下载新模型。

### Q: 支持哪些音频格式？
A: 支持 m4a、mp3、wav、flac 等常见格式。

### Q: macOS 上能否更快？
A: 当前 faster-whisper 不支持 MPS，如需极致性能可考虑 whisper.cpp 或 MLX 框架。

## 技术栈

- [faster-whisper](https://github.com/guillaumekln/faster-whisper)：高效的 Whisper 实现
- [requests](https://requests.readthedocs.io/)：HTTP 请求库
- [uv](https://astral.sh/uv)：现代 Python 包管理和运行工具

## 许可证

本项目仅供学习和个人使用。请遵守播客内容的版权和使用条款。
