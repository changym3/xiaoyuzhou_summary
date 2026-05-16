# Task: 小宇宙播客下载脚本开发

## 日期
2026-05-16

## 任务描述
从小宇宙播客页面下载 m4a 音频文件，并按播客节目和单集标题组织文件结构。

## 实现的功能

### 1. 基础下载功能
- 从播客页面提取 og:audio 中的音频 URL
- 下载音频文件到本地

### 2. 文件命名优化
- 从 JSON-LD 中提取播客节目名称（partOfSeries.name）
- 从 JSON-LD 中提取单集标题（name）
- 使用播客节目名称作为文件夹名
- 使用单集标题作为文件名

### 3. 输出目录管理
- 默认输出目录设置为 `outputs/`
- outputs/ 目录已添加到 .gitignore

### 4. 项目文件整理
- 创建了 `tests/` 目录
- 将所有测试文件和临时文件移到 `tests/` 目录
- 保持项目根目录整洁

## 文件结构

```
asr_project/
├── tests/                    # 测试文件和临时文件
│   ├── check_*.py
│   ├── test_*.py
│   └── ...
├── outputs/                  # 下载的播客文件（gitignore）
│   └── 商业就是这样/
│       └── Vol.84 利乐的"垄断式成功".m4a
├── Task/                     # 任务记录
├── QA/                       # 问答记录
├── download_from_url.py      # 主脚本
└── ...
```

## 修改的文件

1. `/Users/bytedance/trading/asr_project/download_from_url.py`
2. `/Users/bytedance/trading/asr_project/references/xiaoyuzhou-podcast/scripts/download_from_url.py`
3. `/Users/bytedance/trading/asr_project/.gitignore`

## 移动的文件

所有 test_*.py 和 check_*.py 文件已移至 tests/ 目录

## 使用方法

```bash
# 使用默认输出目录（outputs/）
uv run python download_from_url.py "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D"

# 指定自定义输出目录
uv run python download_from_url.py "https://www.xiaoyuzhoufm.com/episode/63508299a526d88c703891a1?s=eyJ1IjoiNjJkZGQ5ZjhlZGNlNjcxMDRhMWQ4ODJjIn0%3D" -o my_downloads
```
