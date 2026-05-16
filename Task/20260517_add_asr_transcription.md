# 2026-05-17 添加语音转写功能

## 任务描述
为 asr_project 项目添加使用 faster-whisper 进行语音转写的功能，支持下载播客后自动转写。

## 架构优化 (2026-05-17)
进行了模块职责分离的架构重构：

### 核心原则
- **单一职责**：每个模块只做一件事
- **完全解耦**：download 和 transcribe 互不依赖
- **统一调度**：main.py 负责流程协调

### 具体修改
1. **download_from_url.py**：移除转写逻辑，只负责下载
2. **transcribe_audio.py**：保持独立，只负责转写
3. **main.py**：作为统一入口，支持下载、转写或两者组合

### 新的使用方式
- `--transcribe` 参数：下载后自动转写
- 独立调用下载：`python download_from_url.py <URL>`
- 独立调用转写：`python transcribe_audio.py <音频文件>`
- 统一入口：`python main.py download/transcribe`

## 性能优化 (2026-05-17)
针对 macOS 平台进行性能优化：
- 默认模型从 medium 改为 small
- 默认设备设置为 cpu
- 调整 beam_size 从 5 到 3，提高速度
- 固定 temperature=0.0，避免多次重试

## macOS 性能建议

### 模型选择建议
| 模型 | 速度 | 准确率 | 适用场景 |
|------|------|--------|----------|
| tiny | 最快 | 一般 | 快速预览 |
| base | 快 | 较好 | 日常使用 |
| **small** | **平衡** | **良好** | **推荐（默认）** |
| medium | 较慢 | 很好 | 高质量需求 |
| large-v3 | 最慢 | 最佳 | 极致质量 |

### 如果需要更快的速度
```bash
# 使用 tiny 模型
uv run python main.py download <URL> --model-size tiny

# 使用 base 模型
uv run python main.py download <URL> --model-size base
```

### 如果需要更高的质量
```bash
# 使用 medium 模型
uv run python main.py download <URL> --model-size medium
```

### 注意
faster-whisper 目前不支持 Apple MPS 加速，如需 Apple Silicon 极致性能可考虑：
- whisper.cpp (CPU 优化)
- MLX 框架 (Apple Silicon 原生)
- CoreML (使用 Neural Engine)

## 实现内容

### 1. 更新依赖配置
- 修改 `pyproject.toml` 添加 `faster-whisper>=1.2.1` 依赖

### 2. 创建转写模块
- 新建 `transcribe_audio.py`，提供核心转写功能
- 支持多种输出格式：txt、srt、json
- 支持词级时间戳和 VAD 静音过滤
- 可配置模型大小、设备、计算类型等参数

### 3. 集成到下载流程
- 修改 `download_from_url.py`，添加转写选项
- 下载完成后自动调用转写功能

### 4. 整合主程序
- 更新 `main.py`，支持子命令模式
- `download` 子命令：下载并转写播客
- `transcribe` 子命令：单独转写已有音频文件

## 使用方法

### 下载并转写播客
```bash
uv run python main.py download <小宇宙播客URL>
```

### 只下载不转写
```bash
uv run python main.py download <URL> --no-transcribe
```

### 单独转写音频文件
```bash
uv run python main.py transcribe <音频文件路径>
```

### 配置转写参数
```bash
uv run python main.py download <URL> --model-size large-v3 --device cuda
```

## 输出目录结构
```
outputs/
  └── [播客名称]/
      ├── [单集标题].m4a      # 音频文件
      ├── [单集标题].txt      # 纯文本转写
      ├── [单集标题].srt      # SRT 字幕格式
      └── [单集标题].json     # 完整 JSON 数据
```
