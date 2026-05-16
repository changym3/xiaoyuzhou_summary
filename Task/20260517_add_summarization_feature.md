# 为项目添加文本总结功能

## 任务概述
为 asr_project 项目添加对转写后文本进行大模型 API 总结的功能。

## 实现步骤
1. 创建 `summarize_text.py` - 独立的文本总结脚本
2. 更新 `pyproject.toml` - 添加必要的依赖（python-dotenv, openai）
3. 修改 `transcribe_audio.py` - 集成总结功能
4. 创建 `.env.example` - 环境变量模板
5. 更新 `.gitignore` - 忽略 .env 文件
6. 创建本文档
7. 创建 QA 文档

## 新增文件
- `summarize_text.py` - 文本总结功能主脚本
- `.env.example` - 环境变量配置模板

## 修改文件
- `pyproject.toml` - 新增依赖
- `transcribe_audio.py` - 集成总结功能
- `.gitignore` - 添加 .env 忽略

## 使用说明

### 1. 配置环境变量
复制 `.env.example` 为 `.env` 并填入实际的 API 配置：
```bash
cp .env.example .env
# 编辑 .env 填入真实信息
```

### 2. 安装依赖
```bash
uv sync
```

### 3. 使用 summarize_text.py 直接总结文本
```bash
uv run python summarize_text.py path/to/text.txt
```

### 4. 使用 transcribe_audio.py 转写并总结
```bash
uv run python transcribe_audio.py --summarize path/to/audio.m4a
```

## 功能特性
- 使用 OpenAI 兼容 API 进行文本总结（支持 Deepseek、OpenAI 等）
- 支持自定义 API 密钥、基础 URL 和模型
- 支持自定义提示词
- 环境变量管理配置信息
- 可独立使用，也可集成到转写流程中

## Deepseek 配置说明
项目已默认配置 Deepseek API：
- API 基础 URL: https://api.deepseek.com
- 默认模型: deepseek-chat
只需在 .env 文件中填入你的 Deepseek API Key 即可使用
