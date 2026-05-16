# QA: 小宇宙播客下载脚本开发

## 日期
2026-05-16

---

## Q1: 实现 tasks.md 中的功能
**用户需求**：实现 tasks.md 中描述的功能，从小宇宙播客页面下载 m4a 文件。

**实现方案**：
- 创建了 `download_from_url.py` 脚本
- 使用 requests 获取页面内容
- 通过正则表达式匹配 `<meta property="og:audio" content="...">` 标签
- 提取音频 URL 并下载

**关键代码**：
```python
audio_pattern = r'<meta\s+property="og:audio"\s+content="([^"]+)"\s*/?>'
audio_match = re.search(audio_pattern, response.text)
```

---

## Q2: 使用节目标题命名文件
**用户需求**：下载的文件应该使用网页中的节目标题命名，而不是默认的文件名。

**实现方案**：
- 从页面的 JSON-LD 数据中提取信息
- `partOfSeries.name` - 播客节目名称（用作文件夹名）
- `name` - 单集标题（用作文件名）

**文件结构**：
```
outputs/
└── 商业就是这样/
    └── Vol.84 利乐的"垄断式成功".m4a
```

---

## Q3: 默认输出到 outputs 目录并添加到 .gitignore
**用户需求**：默认把所有输出都放到 outputs 文件里面，并把 outputs 文件加到 ignore 中。

**实现方案**：
1. 修改脚本默认输出目录从 '.' 改为 'outputs'
2. 在 .gitignore 中添加 `outputs/`

**修改内容**：
```python
parser.add_argument('-o', '--output-dir', default='outputs', help='输出目录（默认：outputs）')
```

**.gitignore 更新**：
```
# Output files
outputs/
```

---

## Q4: 整理项目文件结构
**用户需求**：我想把test文件和check文件整理一下，不想放到项目根目录。

**实现方案**：
- 创建了 `tests/` 目录
- 将所有测试文件移到 `tests/` 目录：
  - check_*.py 文件
  - test_*.py 文件
  - 临时下载的测试文件
- 保持项目根目录整洁

**移动的文件**：
- check_full_page.py
- check_page.py
- check_title.py
- test_download.py
- test_extract.py
- test_folder.py
- test_new_structure.py
- test_outputs_dir.py
- test_rename.py
- test_audio_part.m4a
- 商业就是这样/ (测试下载的文件夹)

---

## 总结

最终实现的功能：
✅ 从小宇宙播客页面提取音频 URL
✅ 使用播客节目名称作为文件夹名
✅ 使用单集标题作为文件名
✅ 默认输出到 outputs/ 目录
✅ outputs/ 目录已添加到 .gitignore
✅ 支持自定义输出目录
✅ 项目文件已整理，测试文件移至 tests/ 目录

使用示例：
```bash
uv run python download_from_url.py "播客页面URL"
```
