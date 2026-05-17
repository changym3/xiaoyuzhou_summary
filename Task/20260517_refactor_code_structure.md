# 代码结构重构

## 问题
用户需求
1. 转录时不应该有 max token 限制，所有录音都应该被转录
2. 代码结构需要优化：download、summary、transcribe 三个文件各司其职，不要互相重叠
3. main 函数统一调度，但调度时各功能独立进行

## 重构方案

### 1. 职责划分
- **download_from_url.py**：只负责下载播客音频
- **transcribe_audio.py**：只负责音频转录，移除所有 summarize 相关逻辑
- **summarize_text.py**：只负责文本总结
- **main.py**：统一调度，支持独立使用和流水线使用

## 修改文件

### 1. transcribe_audio.py
- 移除 `from summarize_text import summarize_file, load_env
- 移除 `transcribe_audio()` 函数中的 `summarize`、`summarize_prompt`、`summarize_max_tokens` 参数
- 移除所有调用 `summarize_file()` 的代码
- 移除命令行参数中的 `--summarize`、`--summarize-prompt`、`--summarize-max-tokens`
- 现在只专注于音频转写功能

### 2. main.py
- 重构为清晰的四个子命令：
  - `download`：只下载
  - `transcribe`：只转录
  - `summarize`：只总结
  - `pipeline`：一站式处理（下载 -> 转录 -> 总结）
- 每个功能独立执行，互不重叠
- 保留智能跳过已完成功能

### 3. download_from_url.py
- 保持不变，已经是独立的

### 4. summarize_text.py
- 保持不变，已经是独立的

## 使用方式

### 独立使用各功能
```bash
# 只下载
uv run python main.py download <url>

# 只转录
uv run python main.py transcribe <audio_path>

# 只总结
uv run python main.py summarize <txt_path>
```

### 流水线处理（一站式）
```bash
# 下载 -> 转录 -> 总结
uv run python main.py pipeline <url>
```

### 也可以直接使用各模块
```bash
uv run python download_from_url.py <url>
uv run python transcribe_audio.py <audio_path>
uv run python summarize_text.py <txt_path>
```

## 架构优势
1. **职责清晰**：每个文件只做一件事
2. **易于维护**：修改一个功能不影响其他功能
3. **灵活使用**：可以独立使用，也可以组合使用
4. **无 token 限制**：转录完全没有 max token 限制（只有总结有，这是正常的

---

## 更新（2026-05-17）：输出格式全面改为 Markdown

### 修改内容
1. **summarize_text.py**：将总结输出格式从 `.txt` 改为 `.md`
2. **transcribe_audio.py**：新增 Markdown (.md) 转写输出格式
3. **main.py**：
   - 更新 summarize_parser 的帮助文本
   - 更新 transcribe_parser 和 pipeline_parser 的 output-formats 选项（包含 'md'）
4. **README.md**：完全更新，反映最新的代码结构和使用方式

### 输出格式说明
- **转写输出**：TXT、Markdown、SRT、JSON 四种格式
  - Markdown 格式包含：文件标题、音频信息、置信度、带时间戳的段落
- **总结输出**：Markdown (.md) 格式，便于阅读和分享

### 优势
- Markdown 格式更适合展示结构化的总结和转写内容
- 与我们新的详细摘要提示词完美配合
- 便于在支持 Markdown 的编辑器中查看

---

## 更新（2026-05-17）：添加 --override 参数

### 修改内容
1. **download_from_url.py**：添加 `--override` 参数，当指定时强制覆盖已存在的音频文件
2. **transcribe_audio.py**：添加 `--override` 参数，当指定时强制覆盖已存在的转写文件
3. **summarize_text.py**：添加 `--override` 参数，当指定时强制覆盖已存在的总结文件
4. **main.py**：所有子命令（download、transcribe、summarize、pipeline）都支持 `--override` 参数
5. **README.md**：更新使用说明，添加 `--override` 示例和常见问题说明

### 使用示例
```bash
# 独立使用时覆盖
uv run python main.py download <url> --override
uv run python main.py transcribe <audio> --override
uv run python main.py summarize <txt> --override

# 流水线时覆盖
uv run python main.py pipeline <url> --override

# 直接使用独立模块时
uv run python download_from_url.py <url> --override
uv run python transcribe_audio.py <audio> --override
uv run python summarize_text.py <txt> --override
```

### 功能说明
- 默认行为：检测到目标文件已存在时，跳过该步骤（智能跳过）
- 加 --override 后：无论文件是否存在，都会强制重新执行并覆盖
- 这个参数给了用户完全的控制权
