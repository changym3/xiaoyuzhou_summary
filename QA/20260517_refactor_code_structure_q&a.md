# 代码结构重构问答

## Q: 为什么要重构代码结构？
A: 原来的代码中，`transcribe_audio.py` 里面包含了 summarize 的逻辑，导致功能重叠，职责不清晰。现在让每个文件只做一件事。

## Q: 转录时还有 max token 限制吗？
A: **没有了！** 转录完全没有 max token 限制，无论多长的音频都会完整转录。只有总结功能有 max_tokens 参数（因为 LLM API 有上下文限制）。

## Q: 三个功能文件的职责是什么？
A:
- **download_from_url.py**：只负责下载播客音频
- **transcribe_audio.py**：只负责音频转写
- **summarize_text.py**：只负责文本总结

## Q: main.py 现在怎么用？
A: main.py 提供了四种使用方式：

1. **独立使用**：
   ```bash
   uv run python main.py download <url>      # 只下载
   uv run python main.py transcribe <audio>   # 只转录
   uv run python main.py summarize <txt>      # 只总结
   ```

2. **流水线处理**：
   ```bash
   uv run python main.py pipeline <url>       # 一站式：下载->转录->总结
   ```

## Q: 还能直接用各模块吗？
A: 可以！各模块依然可以独立运行：
```bash
uv run python download_from_url.py <url>
uv run python transcribe_audio.py <audio>
uv run python summarize_text.py <txt>
```

## Q: 智能跳过功能还在吗？
A: 在的！如果文件已存在，会自动跳过，不会重复处理。

## Q: pipeline 命令包含什么？
A: pipeline 命令按顺序执行三个步骤：
1. 下载播客音频
2. 转录音频为文本
3. 总结文本

每一步都会检查是否已完成，已完成的会跳过。

## Q: 修改了哪些文件？
A:
- **transcribe_audio.py**：移除了 summarize 相关逻辑
- **main.py**：完全重构，支持独立使用和流水线
- **download_from_url.py**：未改动（已经很独立）
- **summarize_text.py**：未改动（已经很独立）

## Q: 重构后的优势是什么？
A:
1. 职责清晰，每个文件只做一件事
2. 易于维护，修改一个功能不影响其他
3. 灵活使用，可以独立用也可以组合用
4. 转录无 token 限制，完整处理所有音频

---

## 更新（2026-05-17）：关于输出格式

## Q: 总结输出格式是什么？
A: 现在总结输出为 **Markdown (.md)** 格式，更适合展示结构化内容。

## Q: 转写输出格式呢？
A: 转写现在支持四种格式：
- **TXT**：纯文本
- **Markdown (.md)**：结构化格式，带时间戳标题
- **SRT**：字幕格式
- **JSON**：完整数据

## Q: 为什么转写也支持 Markdown 格式？
A:
- Markdown 格式的转写包含文件标题、音频信息、置信度
- 每个段落带时间戳，便于定位
- 与总结的总结格式统一，便于查看

## Q: 这次还更新了什么？
A: 完全重写了 README.md，反映最新的代码结构和使用方式，包括：
- 更新了 main.py 中 summarize_parser 的帮助文本
- 更新了所有 output-formats 的选项

---

## 更新（2026-05-17）：--override 参数

## Q: 什么是 --override 参数？
A: 是一个新增的命令行参数，当指定这个参数时，无论目标文件是否存在，都会强制重新执行并覆盖已存在的文件。

## Q: 什么时候需要用 --override？
A: 当你想要：
1. 重新下载已经下载过的音频
2. 重新转写已经转写过的文件
3. 重新总结已经总结过的文本
4. 在流水线中强制重新运行所有步骤

## Q: 所有命令都支持 --override 吗？
A: 是的！所有命令都支持：
- `download`：覆盖已下载的音频
- `transcribe`：覆盖已转写的文件
- `summarize`：覆盖已总结的文件
- `pipeline`：覆盖所有中间文件

## Q: 使用 --override 的例子？
A:
```bash
# 独立使用
uv run python main.py download <url> --override

# 流水线
uv run python main.py pipeline <url> --override

# 直接使用模块
uv run python download_from_url.py <url> --override
```

## Q: 默认行为是怎样的？
A: 默认会智能跳过：
- 如果文件已存在，不重复处理
- 这样可以节省时间和资源

## Q: --override 和智能跳过后会冲突吗？
A: 不会冲突！
- 默认：有文件则跳过（智能跳过）
- 加 --override：不管有没有文件都重新执行

## Q: 修改了哪些文件来支持 --override？
A:
- **download_from_url.py**：添加 override 参数和逻辑
- **transcribe_audio.py**：添加 override 参数和逻辑
- **summarize_text.py**：添加 override 参数和逻辑
- **main.py**：所有子命令都支持 override 参数
- **README.md**：添加使用说明和示例
