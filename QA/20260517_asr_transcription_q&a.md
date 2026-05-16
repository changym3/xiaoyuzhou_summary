# 2026-05-17 语音转写功能问答

## 架构相关

### Q: 为什么要把 download 和 transcribe 分开？
A: 单一职责原则，让每个模块只做一件事，代码更清晰、更易维护、更易测试。download 负责下载，transcribe 负责转写，main 负责调度。

### Q: 模块之间有依赖吗？
A: 没有。download_from_url.py 和 transcribe_audio.py 完全独立，可以单独使用，互不依赖。

## 使用方式

### Q: 如何下载并转写？
A: 使用 `--transcribe` 参数：`uv run python main.py download <URL> --transcribe`

### Q: 如何只下载不转写？
A: 默认就是只下载：`uv run python main.py download <URL>`

### Q: 如何只转写已有音频？
A: `uv run python main.py transcribe <音频文件>`

### Q: 能单独调用 download_from_url.py 吗？
A: 可以：`uv run python download_from_url.py <URL>`，它是独立的下载脚本。

### Q: 能单独调用 transcribe_audio.py 吗？
A: 可以：`uv run python transcribe_audio.py <音频文件>`，它是独立的转写模块。

## 功能相关

### Q: 如何安装新添加的依赖？
A: 运行 `uv sync` 安装 faster-whisper 及相关依赖。

### Q: 首次使用需要注意什么？
A: 首次运行会自动从 Hugging Face Hub 下载 small 模型（约 500MB），请确保网络连接正常。

### Q: macOS 上为什么这么慢？
A: faster-whisper 目前不支持 Apple MPS (Metal) 加速，只能使用 CPU。我们已优化默认配置使用 small 模型，平衡了速度和准确率。

### Q: 如何在 macOS 上获得更快的转写？
A: 
- 使用 `--model-size tiny` 最快，但准确率一般
- 使用 `--model-size base` 速度和准确率平衡较好
- 如果需要极致性能，可考虑使用 MLX 或 whisper.cpp 等 Apple Silicon 专用工具

### Q: 不同模型大小差异如何？
A: 
| 模型 | 大小 | 速度 |
|------|------|------|
| tiny | ~150MB | 最快 |
| base | ~300MB | 快 |
| small | ~500MB | 中等（默认） |
| medium | ~1.5GB | 较慢 |
| large-v3 | ~3GB | 最慢 |

### Q: 支持哪些音频格式？
A: 支持 m4a、mp3、wav、flac 等常见格式，通过 PyAV 处理。

### Q: 没有 GPU 怎么办？
A: 使用 CPU 模式，`--device cpu --compute-type int8`，速度较慢但可用。

### Q: 词级时间戳有什么用？
A: 可以定位到具体每个词的时间位置，便于内容查找和剪辑。

### Q: 输出的三种格式各有什么特点？
A:
- TXT：纯文本，最易读
- SRT：字幕格式，带时间戳
- JSON：完整数据，含词级时间戳和元数据
