<div align="center">

# 🚀 AI Content Multiplatform

### 一次创作，7 平台智能适配

[![GitHub Stars](https://img.shields.io/github/stars/JianFeiGan/ai-content-multiplatform?style=social)](https://github.com/JianFeiGan/ai-content-multiplatform/stargazers)
[![PyPI Downloads](https://img.shields.io/pypi/dm/ai-content-multiplatform.svg)](https://pypi.org/project/ai-content-multiplatform/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-v0.2.0-orange.svg)](https://pypi.org/project/ai-content-multiplatform/)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/JianFeiGan/ai-content-multiplatform/actions/workflows/test.yml/badge.svg)](https://github.com/JianFeiGan/ai-content-multiplatform/actions/workflows/test.yml)

**写一篇 → 适配7个平台 → 自动导出** · AI 驱动，GPT 智能改写，不仅是截断

[English](#) · [快速开始](#快速开始) · [在线演示](#使用效果) · [贡献指南](CONTRIBUTING.md)

</div>

---

## 😫 你是不是也这样？

> 写了一篇好文章，发到微信要改格式，发到知乎要改风格，发到小红书要加 Emoji 和标签，发到 CSDN 要调代码块…
>
> **同样一篇内容，手动适配 7 个平台，3 小时起步。**

**ai-content-multiplatform** 解决的就是这个问题：

| ❌ 之前 | ✅ 现在 |
|---------|---------|
| 一篇内容手动改 7 遍 | 一条命令适配 7 个平台 |
| 每个平台规则都要记 | 内置 7 大平台规则引擎 |
| 标题/标签/长度手动调 | AI 智能改写，风格自适应 |
| 禁用词踩坑被限流 | 自动过滤平台禁用词 |
| 格式不兼容反复调 | 按平台规范自动格式化 |

---

## ✨ 使用效果

一条命令，7 个平台瞬间搞定：

```bash
ai-content-multiplatform adapt file article.md -p all
```

**输入**：一篇标准 Markdown 文章

**输出**：7 份平台定制内容

| 平台 | 适配后标题 | 风格 |
|------|-----------|------|
| 🟢 微信公众号 | 🔥 程序员注意！这个AI工具正在... | 悬念感 + 短段落 + 手机阅读 |
| 🔵 知乎 | 大语言模型在多平台内容适配中的实践 | 专业深度 + 数据引用 + 逻辑严密 |
| 🟠 CSDN | Python实现AI内容多平台适配工具 | 技术导向 + 代码示例 + 解决方案 |
| ⚫ 抖音 | 你知道吗？3小时变3秒的秘密 | 口语化 + 节奏感 + 30秒口播 |
| 🔴 小红书 | AI写作神器🔥一篇文变7篇！ | 轻松活泼 + Emoji + 短句分段 |
| 🔵 掘金 | 深入理解LLM内容适配引擎设计 | 技术深度 + 实战 + 踩坑记录 |
| 🔴 头条号 | AI工具正在改变内容创作方式 | 通俗冲击 + 大众科普 |

---

## 🎯 特性

- 🌐 **7 平台全覆盖** — 微信公众号、知乎、CSDN、抖音、小红书、掘金、头条号
- 🤖 **AI 智能适配 (v0.2.0)** — 接入 OpenAI GPT-4o-mini，根据平台 Prompt **智能改写**内容（不仅是简单的截断）
- ⚡ **CLI 命令行工具** — 简洁高效的命令行界面，支持文件输入、文本输入、预览、导出
- 📦 **批量处理** — 一键将内容适配到所有支持的平台，异步并发执行
- 📋 **规则配置系统** — YAML 格式的平台规则，包含标题长度、内容限制、封面尺寸、风格提示词、禁用词
- 📤 **多格式导出** — 自动根据平台特性导出格式（如小红书带 Emoji/标签，微信带 Markdown 排版）
- 🏃 **Dry Run 模式** — 仅显示适配计划，不实际调用 API，方便调试
- 🎨 **终端美化** — 基于 Rich 库，输出带有颜色、表格、面板等可视化元素
- 📝 **类型安全** — 全量类型注解 + Pydantic 数据验证 + MyPy 类型检查
- 🚀 **现代构建工具** — 使用 `uv` 进行依赖管理和打包构建，速度极快

---

## 快速开始

安装后立即体验：

```bash
# 1. 安装（推荐使用 uv 进行极速安装）
uv tool install ai-content-multiplatform

# 或者使用传统的 pip
pip install ai-content-multiplatform

# 2. 配置 OpenAI API Key
export OPENAI_API_KEY="sk-xxx"

# 3. 适配一篇内容到所有平台
ai-content-multiplatform adapt file examples/sample.md -p all
```

```
$ ai-content-multiplatform adapt file examples/sample.md -p all

📖 读取内容：examples/sample.md
📝 解析完成：大语言模型如何重塑内容创作工作流 (3256 字符)
🎯 目标平台：weixin, zhihu, csdn, douyin, xiaohongshu, juejin, toutiao
🔄 开始适配...
  → 适配 weixin... ✓
  → 适配 zhihu... ✓
  → 适配 csdn... ✓
  → 适配 douyin... ✓
  → 适配 xiaohongshu... ✓
  → 适配 juejin... ✓
  → 适配 toutiao... ✓

 ╭────────────────── ✅ 适配完成 ───────────────────╮
 │ 平台        │ 标题               │ 内容长度  │ 标签数 │
 ├─────────────┼────────────────────┼───────────┼───────┤
 │ weixin      │ 🔥 程序员注意！这...│ 2856 字符  │ 5     │
 │ zhihu       │ 大语言模型在多平台...│ 4120 字符  │ 4     │
 │ csdn        │ Python实现AI内容多...│ 3200 字符  │ 8     │
 │ douyin      │ 你知道吗？你花3小...│ 280 字符   │ 10    │
 │ xiaohongshu │ AI写作神器🔥一篇文...│ 650 字符   │ 8     │
 │ juejin      │ 深入理解LLM内容适...│ 3800 字符  │ 4     │
 │ toutiao     │ AI工具正在改变内...│ 2100 字符  │ 3     │
 ╰──────────────────────────────────────────────────╯
```

---

## 安装指南

### 方式一：从 PyPI 安装（推荐）

推荐使用 `pipx` 或 `uv` 进行隔离安装，避免污染系统环境：

```bash
# 使用 uv (推荐，速度极快)
uv tool install ai-content-multiplatform

# 或者使用 pip
pip install ai-content-multiplatform
```

### 方式二：从源码安装

```bash
git clone https://github.com/JianFeiGan/ai-content-multiplatform.git
cd ai-content-multiplatform
uv pip install .
```

### 方式三：开发模式安装

```bash
git clone https://github.com/JianFeiGan/ai-content-multiplatform.git
cd ai-content-multiplatform
uv sync --all-groups
```

> **前置要求**：Python 3.11+ 已安装。

### 环境变量配置

创建 `.env` 文件（或设置环境变量）：

```env
# OpenAI API 配置
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.openai.com/v1

# 应用配置（可选，有默认值）
AI_CONTENT_DEFAULT_MODEL=gpt-4o-mini
AI_CONTENT_DEFAULT_TEMPERATURE=0.7
```

---

## 使用文档

### adapt — 内容适配

将 Markdown 文件或文本内容适配到指定平台。

#### 从文件适配

```bash
# 适配到所有平台
ai-content-multiplatform adapt file input.md -p all

# 适配到指定平台（逗号分隔）
ai-content-multiplatform adapt file input.md -p weixin,zhihu,csdn

# 指定输出目录
ai-content-multiplatform adapt file input.md -p all -o ./output/

# Dry Run 模式（仅显示适配计划）
ai-content-multiplatform adapt file input.md -p all --dry-run
```

| 参数 | 短选项 | 默认值 | 说明 |
|------|--------|--------|------|
| `input_file` | — | 必需 | 输入 Markdown 文件路径 |
| `--platforms` | `-p` | `all` | 目标平台，逗号分隔或 `all` |
| `--output` | `-o` | 配置默认值 | 输出目录路径 |
| `--dry-run` | — | `False` | 仅显示适配计划，不执行 |

#### 从文本适配

```bash
# 直接传入文本
ai-content-multiplatform adapt text "这是一段测试内容" -t "测试标题" -p weixin

# 结合命令行管道使用
echo "文章内容..." | ai-content-multiplatform adapt text -t "标题" -p zhihu
```

| 参数 | 短选项 | 默认值 | 说明 |
|------|--------|--------|------|
| `text` | — | 必需 | 输入文本内容 |
| `--title` | `-t` | `""` | 内容标题 |
| `--platforms` | `-p` | `all` | 目标平台 |

#### 输入文件格式

支持的 Markdown 文件格式（可选 YAML front matter）：

```markdown
---
title: "文章标题"
tags:
  - AI
  - 技术
  - 教程
author: "作者名"
---

# 正文标题

这里是正文内容，支持标准 Markdown 语法...
```

### preview — 预览效果

预览内容在指定平台的适配效果，不保存文件。

```bash
ai-content-multiplatform preview content input.md weixin
```

输出示例：

```
🔍 预览 weixin 适配效果

 ╭──────────── 📱 weixin 预览 ────────────╮
 │ 标题：🔥 程序员注意！这个AI工具正在...   │
 │                                          │
 │ 内容：                                    │
 │ 你知道吗？现在只要输入一篇文章，AI...      │
 │                                          │
 │ 标签：AI, 效率工具, 自动化, 内容创作     │
 ╰──────────────────────────────────────────╯
```

### publish — 导出内容

将内容文件直接导出为各平台专用格式。

```bash
# 导出到所有平台
ai-content-multiplatform publish input.md -p all

# 导出到指定平台
ai-content-multiplatform publish input.md -p xiaohongshu,zhihu -o ./my_exports/

# 导出并启用 LLM 二次适配
ai-content-multiplatform publish input.md -p all --llm
```

### config — 配置管理

```bash
ai-content-multiplatform config
```

---

## 平台规则说明

每个平台都有独特的内容规范：

| 平台 | 标识 | 标题上限 | 内容上限 | 标签上限 | 封面尺寸 | 风格特点 |
|------|------|---------|---------|---------|---------|---------|
| **🟢 微信公众号** | `weixin` | 64 | 20,000 | 0 | 900×383 | 悬念感标题、短段落、手机阅读优化 |
| **🔵 知乎** | `zhihu` | 100 | 100,000 | 5 | 1920×1080 | 专业深度、逻辑严密、引用数据 |
| **🟠 CSDN** | `csdn` | 100 | 50,000 | 10 | 1080×720 | 技术导向、代码示例、解决方案 |
| **⚫ 抖音** | `douyin` | 30 | 300 | 15 | 1080×1920 | 口语化、节奏感、30-60秒口播 |
| **🔴 小红书** | `xiaohongshu` | 20 | 1,000 | 10 | 1242×1660 | 轻松活泼、emoji丰富、短句分段 |
| **🔵 掘金** | `juejin` | 100 | 50,000 | 5 | 1200×630 | 技术深度、实战导向、踩坑记录 |
| **🔴 头条号** | `toutiao` | 30 | 50,000 | 5 | 1280×720 | 通俗冲击、大众科普、新闻资讯 |

### 禁用词自动过滤

- **微信公众号**：`微信`、`朋友圈`、`点赞`
- **知乎**：`微信`、`扫码`、`私聊`
- **小红书**：`微信`、`淘宝`、`京东`
- **CSDN**：`转载`、`搬运`
- **头条号**：`微信`、`公众号`

> 💡 禁用词会在适配过程中自动过滤，确保内容符合平台规范。

---

## 配置说明

### 环境变量

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `OPENAI_API_KEY` | — | OpenAI API Key（必需） |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | API 基础 URL |
| `AI_CONTENT_DEFAULT_MODEL` | `gpt-4o-mini` | 默认 LLM 模型 |
| `AI_CONTENT_DEFAULT_TEMPERATURE` | `0.7` | 生成温度 |

### 自定义规则文件

```yaml
# my-rules.yaml
platforms:
  weixin:
    name: "微信公众号"
    title_max_len: 64
    content_max_len: 20000
    style_prompt: |
      自定义的微信公众号风格提示词...
    forbidden_words: ["微信", "朋友圈"]
```

---

## 架构说明

```
┌─────────────────────────────────────────────────────────┐
│                    CLI 层 (Typer)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │
│  │  adapt   │  │ preview  │  │ publish  │  │ config  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘  │
└───────┼─────────────┼─────────────┼─────────────┼───────┘
        │             │             │             │
┌───────▼─────────────▼─────────────▼─────────────▼───────┐
│                   核心处理层                              │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ ContentParser│  │ContentAdapter│  │ContentPubl.  │  │
│  │              │  │              │  │              │  │
│  │ • parse_file │  │ • adapt()    │  │ • publish()  │  │
│  │ • parse_text │  │ • validate() │  │ • draft()    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
└─────────┼─────────────────┼─────────────────┼───────────┘
          │                 │                 │
┌─────────▼─────────────────▼─────────────────▼───────────┐
│                   数据/配置层                              │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Pydantic   │  │   Settings  │  │   Platform      │  │
│  │   Models    │  │  (pydantic- │  │   Rules         │  │
│  │             │  │   settings) │  │   (YAML)        │  │
│  │ • Content   │  │             │  │                 │  │
│  │ • Adapted   │  │ • .env      │  │ • 7 platforms   │  │
│  │ • Platform  │  │ • defaults  │  │ • forbidden     │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
          │                                  │
┌─────────▼──────────────┐    ┌──────────────▼────────────┐
│   OpenAI API           │    │   外部平台 API              │
│   (LLM 适配引擎)        │    │   (发布/草稿)              │
└────────────────────────┘    └───────────────────────────┘
```

### 数据流

```
Markdown 输入 → ContentParser.parse_file() → ContentInput
                                              ↓
                                    ContentAdapter.adapt()
                                    （调用 OpenAI API + 规则校验）
                                              ↓
                                       AdaptedContent
                                              ↓
                              Formatter.save() → 输出文件
```

---

## API 文档

### 核心类

#### ContentInput

```python
from ai_content_multiplatform.core.models import ContentInput

content = ContentInput(
    title="AI 如何改变内容创作",
    content="# 正文内容...\n这里是正文...",
    tags=["AI", "内容创作"],
    author="作者名",
)
```

#### PlatformRule

```python
from ai_content_multiplatform.core.models import PlatformRule

rule = PlatformRule(
    name="微信公众号",
    title_max_len=64,
    content_max_len=20000,
    tag_limit=0,
    cover_size=(900, 383),
    style_prompt="微信公众号风格：标题要吸引眼球...",
    forbidden_words=["微信", "朋友圈"],
)
```

#### AdaptedContent

```python
from ai_content_multiplatform.core.models import AdaptedContent

adapted = AdaptedContent(
    platform="weixin",
    platform_name="微信公众号",
    title="🔥 这个AI工具正在改变内容行业",
    title_candidates=["备选标题1", "备选标题2"],
    content="适配后的正文内容...",
    tags=["AI", "效率工具"],
)
```

### 工具函数

```python
from ai_content_multiplatform.utils.formatter import (
    strip_markdown,
    truncate_text,
    strip_forbidden_words,
)

# 移除 Markdown 标记
plain = strip_markdown("**粗体** 和 [链接](url)")
# → "粗体 和 链接"

# 截断文本
short = truncate_text("这是一段很长的文本...", max_len=10)
# → "这是一段很..."

# 移除禁用词
clean = strip_forbidden_words("微信扫码关注", ["微信"])
# → "扫码关注"
```

---

## 示例文件

```bash
# 使用示例文件进行适配
ai-content-multiplatform adapt file examples/sample.md -p all

# 预览示例在某个平台的效果
ai-content-multiplatform preview content examples/sample.md xiaohongshu
```

---

## FAQ

### 如何配置 LLM API？

```bash
# 方式一：命令行
export OPENAI_API_KEY="sk-xxx"

# 方式二：.env 文件
echo 'OPENAI_API_KEY=sk-xxx' > .env

# 方式三：使用兼容 API
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="sk-xxx"
```

### 支持哪些 LLM 模型？

默认 `gpt-4o-mini`（性价比高）。也支持 `gpt-4o`、`gpt-3.5-turbo` 及任何 OpenAI 兼容 API 的模型。

### 如何自定义平台规则？

1. 复制默认规则文件并修改
2. 在代码中加载：`settings.load_rules("./my-rules.yaml")`

### 适配质量不满意？

- 调整 `temperature`（0.3-0.9）
- 修改 `rules.yaml` 中的 `style_prompt`
- 用 `preview` 先预览再批量适配

### 支持哪些 Python 版本？

Python 3.11+，推荐 3.12。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request，特别是添加新的平台适配器！

### 贡献流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
feat: 新增功能 | fix: 修复 bug | docs: 文档更新
style: 代码格式 | refactor: 重构 | test: 测试 | chore: 构建
```

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 开发环境设置

```bash
# 克隆项目
git clone https://github.com/JianFeiGan/ai-content-multiplatform.git
cd ai-content-multiplatform

# 安装依赖（含 dev 组）
uv sync --all-extras

# 运行测试
uv run pytest

# 代码检查
uv run ruff check src/ tests/

# 类型检查
uv run mypy src/

# 构建打包
uv build
```

---

## 📄 许可证

[MIT License](LICENSE) © 2026 Hermes AI

---

<div align="center">

**⭐ 如果这个项目对你有帮助，欢迎在 GitHub 上给个 Star！**

[GitHub](https://github.com/JianFeiGan/ai-content-multiplatform) · [PyPI](https://pypi.org/project/ai-content-multiplatform/) · [Issues](https://github.com/JianFeiGan/ai-content-multiplatform/issues)

</div>
