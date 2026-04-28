# ai-content-multiplatform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/badge/pypi-v0.2.0-orange.svg)](https://pypi.org/project/ai-content-multiplatform/)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/JianFeiGan/ai-content-multiplatform/actions/workflows/test.yml/badge.svg)](https://github.com/JianFeiGan/ai-content-multiplatform/actions/workflows/test.yml)

> **一次创作，多平台适配。** AI 驱动的内容多平台适配与发布工具，将核心内容智能适配到微信公众号、知乎、CSDN、抖音、小红书、掘金、头条号等 7 大平台。

---

## 目录

- [特性](#特性)
- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [使用文档](#使用文档)
  - [adapt — 内容适配](#adapt--内容适配)
  - [preview — 预览效果](#preview--预览效果)
  - [publish — 导出内容](#publish--导出内容)
  - [config — 配置管理](#config--配置管理)
- [平台规则说明](#平台规则说明)
- [配置说明](#配置说明)
- [架构说明](#架构说明)
- [API 文档](#api-文档)
- [示例文件](#示例文件)
- [FAQ 常见问题](#faq-常见问题)
- [贡献指南](#贡献指南)
- [开发环境设置](#开发环境设置)
- [许可证](#许可证)

---

## 特性

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

# 2. 配置 OpenAI API Key（推荐使用 .env 文件）
export OPENAI_API_KEY="your-api-key-here"

# 3. 查看帮助
ai-content-multiplatform --help
```

```
$ ai-content-multiplatform --help

 ╭─────────────────────────────────────────╮
 │  AI Content Multiplatform v0.2.0        │
 │  AI 内容多平台适配与发布工具              │
 ╰─────────────────────────────────────────╯

 Usage: ai-content-multiplatform [COMMAND]

 Commands:
   adapt     适配内容到多平台
   preview   预览适配效果
   publish   发布内容到指定平台
   config    显示当前配置
   init      初始化默认配置文件
```

适配一个 Markdown 文件到所有平台：

```bash
ai-content-multiplatform adapt file examples/sample.md -p all
```

输出效果示意：

```
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
  💾 已保存：output/weixin_大语言模型如何重塑内容创作工作流：从单点到多平.md
  ...

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

本项目推荐使用 `uv` 进行开发依赖管理：

```bash
git clone https://github.com/JianFeiGan/ai-content-multiplatform.git
cd ai-content-multiplatform

# 同步所有依赖（包括 dev 组）
uv sync --all-groups

# 或者直接安装开发模式
uv pip install -e ".[dev]"
```

> **前置要求**：Python 3.11+ 已安装。如果未安装 `uv`，请参考 [uv 官方文档](https://docs.astral.sh/uv/) 进行安装。

### 环境变量配置

创建 `.env` 文件（或设置环境变量）：

```env
# OpenAI API 配置
OPENAI_API_KEY=sk-your-api-key-here
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

| 参数 | 说明 |
|------|------|
| `input_file` | 输入内容文件路径 |
| `platform` | 目标平台标识 |

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

将内容文件直接导出为各平台专用格式（无需经过适配步骤，适用于已有内容文件的快速导出）。

```bash
# 导出到所有平台（默认输出到 ./output 目录）
ai-content-multiplatform publish input.md -p all

# 导出到指定平台并指定输出目录
ai-content-multiplatform publish input.md -p xiaohongshu,zhihu -o ./my_exports/

# 导出并启用 LLM 进行二次适配
ai-content-multiplatform publish input.md -p all --llm
```

| 参数 | 短选项 | 默认值 | 说明 |
|------|--------|--------|------|
| `input_file` | — | 必需 | 输入 Markdown 文件路径 |
| `--platforms` | `-p` | `all` | 目标平台，逗号分隔或 `all` |
| `--output` | `-o` | `./output` | 导出文件保存目录 |
| `--llm` | — | `False` | 发布前使用 LLM 重新智能适配 |

### config — 配置管理

查看当前应用配置。

```bash
ai-content-multiplatform config
```

### 平台规则说明

每个平台都有独特的内容规范。以下是各平台的详细规则：

| 平台 | 标识 | 标题上限 | 内容上限 | 标签上限 | 封面尺寸 | 风格特点 |
|------|------|---------|---------|---------|---------|---------|
| **微信公众号** | `weixin` | 64 | 20,000 | 0 | 900×383 | 悬念感标题、短段落、手机阅读优化 |
| **知乎** | `zhihu` | 100 | 100,000 | 5 | 1920×1080 | 专业深度、逻辑严密、引用数据 |
| **CSDN** | `csdn` | 100 | 50,000 | 10 | 1080×720 | 技术导向、代码示例、解决方案 |
| **抖音** | `douyin` | 30 | 300 | 15 | 1080×1920 | 口语化、节奏感、30-60秒口播 |
| **小红书** | `xiaohongshu` | 20 | 1,000 | 10 | 1242×1660 | 轻松活泼、emoji丰富、短句分段 |
| **掘金** | `juejin` | 100 | 50,000 | 5 | 1200×630 | 技术深度、实战导向、踩坑记录 |
| **头条号** | `toutiao` | 30 | 50,000 | 5 | 1280×720 | 通俗冲击、大众科普、新闻资讯 |

### 禁用词示例

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

你可以创建自定义的规则文件来覆盖默认行为：

```yaml
# my-rules.yaml
platforms:
  weixin:
    name: "微信公众号"
    title_max_len: 64
    content_max_len: 20000
    tag_limit: 0
    cover_size: [900, 383]
    style_prompt: |
      自定义的微信公众号风格提示词...
    forbidden_words: ["微信", "朋友圈"]

defaults:
  llm_model: "gpt-4o"
  temperature: 0.5
  max_tokens: 4000
  title_candidates: 5
```

### 默认 LLM 配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `llm_model` | `gpt-4o-mini` | 使用的 LLM 模型 |
| `temperature` | `0.7` | 创造性参数（0=确定性，1=创造性） |
| `max_tokens` | `4000` | 最大生成长度 |
| `title_candidates` | `3` | 每个平台生成的备选标题数 |

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

### 模块说明

| 模块 | 路径 | 职责 |
|------|------|------|
| **CLI 层** | `src/.../cli/` | 命令行入口，Typer 路由 |
| **核心模型** | `src/.../core/models.py` | Pydantic 数据模型（ContentInput, PlatformRule, AdaptedContent） |
| **配置管理** | `src/.../config/` | Settings（环境变量）+ rules.yaml（平台规则） |
| **工具函数** | `src/.../utils/` | 格式化（strip_markdown, truncate_text）+ 日志 |
| **平台规则** | `src/.../config/rules.yaml` | 7 个平台的详细规则配置 |

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

用户输入的原始内容模型。

```python
from ai_content_multiplatform.core.models import ContentInput

content = ContentInput(
    title="AI 如何改变内容创作",
    content="# 正文内容...\n这里是正文...",
    tags=["AI", "内容创作"],
    author="作者名",
    images=["https://example.com/image.jpg"],
)
```

#### PlatformRule

单个平台的适配规则。

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
    notes="不支持 Markdown 格式",
)
```

#### AdaptedContent

适配后的单平台内容。

```python
from ai_content_multiplatform.core.models import AdaptedContent

adapted = AdaptedContent(
    platform="weixin",
    platform_name="微信公众号",
    title="🔥 这个AI工具正在改变内容行业",
    title_candidates=["备选标题1", "备选标题2", "备选标题3"],
    content="适配后的正文内容...",
    tags=["AI", "效率工具"],
    cover_suggestion="AI 机器人与创作者协作的插图",
)
```

#### AppConfig

全局配置管理类。

```python
from ai_content_multiplatform.config.settings import AppConfig

# 从环境变量/配置文件加载
settings = AppConfig()

# 加载平台规则
rules_config = settings.load_rules()
platform_rules = settings.get_platform_rules()

# 获取单个平台规则
weixin_rule = platform_rules["weixin"]
print(f"标题上限：{weixin_rule.title_max_len}")
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

### 日志工具

```python
from ai_content_multiplatform.utils.logger import get_logger

logger = get_logger(__name__, level="DEBUG")
logger.info("这是一条信息日志")
logger.debug("这是一条调试日志")
```

---

## 示例文件

项目提供了示例输入文件，位于 `examples/sample.md`：

```bash
# 使用示例文件进行适配
ai-content-multiplatform adapt file examples/sample.md -p all

# 预览示例在某个平台的效果
ai-content-multiplatform preview content examples/sample.md xiaohongshu
```

示例文件包含：
- YAML front matter（title, tags, author, date）
- 完整的 Markdown 正文（标题、引用、列表、表格、代码块）
- 适合作为演示和测试的输入内容

---

## FAQ 常见问题

### Q1: 如何配置 LLM API？

设置环境变量 `OPENAI_API_KEY`：

```bash
# 方式一：命令行
export OPENAI_API_KEY="sk-..."

# 方式二：.env 文件
echo 'OPENAI_API_KEY=sk-...' > .env

# 方式三：使用兼容 API（如本地部署）
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="not-needed"
```

### Q2: 支持哪些 LLM 模型？

默认使用 `gpt-4o-mini`（性价比高）。你也可以使用：
- `gpt-4o` — 质量更高，成本更高
- `gpt-3.5-turbo` — 速度快，成本低
- 任何 OpenAI 兼容 API 的模型

在 `.env` 中配置：
```env
AI_CONTENT_DEFAULT_MODEL=gpt-4o
```

### Q3: 如何自定义平台规则？

1. 复制默认规则文件：
```bash
cp $(python -c "import ai_content_multiplatform.config; from pathlib import Path; print(Path(ai_content_multiplatform.config.__file__).parent / 'rules.yaml')") ./my-rules.yaml
```

2. 编辑 `my-rules.yaml`，修改平台参数
3. 在代码中加载自定义规则：
```python
settings = AppConfig()
rules = settings.load_rules("./my-rules.yaml")
```

### Q4: 适配质量不满意怎么办？

- 调整 `temperature` 参数（0.3-0.9 范围），较低值更稳定
- 修改 `rules.yaml` 中的 `style_prompt`，提供更详细的风格描述
- 在 front matter 中增加更多上下文信息（tags, author）
- 使用 `preview` 命令先预览效果，满意后再批量适配

### Q5: 发布功能需要配置什么？

发布功能需要配置各平台的 API 凭据。目前支持：
- 草稿模式（无需 API，仅本地保存）
- 自动发布（需要对应平台的 API Token）

在 `.env` 中配置对应平台的 Token：
```env
# 微信公众号
WEIXIN_APP_ID=xxx
WEIXIN_APP_SECRET=xxx

# 知乎
ZHIHU_ACCESS_TOKEN=xxx
```

### Q6: 支持哪些 Python 版本？

Python 3.11+。推荐使用 Python 3.12 以获得最佳性能。

### Q7: 离线环境能用吗？

内容适配需要调用 OpenAI API，因此需要网络连接。如果只是解析和格式化（不调用 LLM），可以在离线环境使用 `--dry-run` 模式。

### Q8: 如何贡献代码？

欢迎 PR！请参阅下方的 [贡献指南](#贡献指南)。

---

## 贡献指南

### 贡献流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'feat: add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 提交 Pull Request

### 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 新增功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构代码
test: 测试相关
chore: 构建/工具链
```

### 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 关注社区整体利益

---

## 开发环境设置

本项目推荐使用 **[uv](https://docs.astral.sh/uv/)** 进行环境管理和构建。

### 1. 克隆项目

```bash
git clone https://github.com/JianFeiGan/ai-content-multiplatform.git
cd ai-content-multiplatform
```

### 2. 初始化环境

`uv` 会自动管理虚拟环境和 Python 版本：

```bash
# 自动创建虚拟环境并安装所有依赖（含 dev 组）
uv sync --all-extras
```

### 3. 运行测试

所有命令需通过 `uv run` 执行，以确保使用项目隔离的依赖环境：

```bash
# 运行全部测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=ai_content_multiplatform --cov-report=html

# 查看 HTML 覆盖率报告
open htmlcov/index.html  # macOS
```

### 4. 代码规范检查

```bash
# Ruff 检查
uv run ruff check src/ tests/

# Ruff 自动修复
uv run ruff check --fix src/ tests/

# Ruff 格式化
uv run ruff format src/ tests/

# MyPy 类型检查
uv run mypy src/
```

### 5. 本地构建与打包

使用 `uv` 构建 Wheel 和源码分发包：

```bash
# 构建项目 (生成 dist/*.whl 和 dist/*.tar.gz)
uv build

# 检查包内容
tar -tzf dist/ai_content_multiplatform-*.tar.gz | head -n 20
```

### 项目结构

```
ai-content-multiplatform/
├── src/
│   └── ai_content_multiplatform/
│       ├── __init__.py
│       ├── cli/                    # CLI 命令行工具
│       │   ├── main.py             # 入口 & 主命令
│       │   ├── adapt.py            # adapt 子命令
│       │   ├── preview.py          # preview 子命令
│       │   └── publish.py          # publish 子命令
│       ├── config/                 # 配置管理
│       │   ├── __init__.py
│       │   ├── settings.py         # Settings & AppConfig
│       │   └── rules.yaml          # 平台规则配置
│       ├── core/                   # 核心逻辑
│       │   ├── __init__.py
│       │   └── models.py           # Pydantic 数据模型
│       └── utils/                  # 工具函数
│           ├── __init__.py
│           ├── formatter.py        # 文本格式化
│           └── logger.py           # 日志配置
├── tests/                          # 测试文件
│   └── __init__.py
├── examples/                       # 示例文件
│   └── sample.md
├── docs/                           # 项目文档
│   ├── 01-business-requirements.md
│   ├── 02-technical-design.md
│   └── 03-self-review.md
├── .github/workflows/              # CI/CD
│   ├── test.yml
│   └── release.yml
├── pyproject.toml                  # 项目配置
├── CHANGELOG.md                    # 变更日志
├── LICENSE                         # MIT 许可证
├── README.md                       # 本文档
└── .gitignore                      # Git 忽略规则
```

---

---

## 📂 示例与最佳实践

我们提供了一些真实的输入输出示例，帮助你快速理解各平台的风格差异：

- **输入示例**: [`examples/sample.md`](examples/sample.md) — 一篇标准的通用技术文章。
- **小红书输出**: [`examples/output_xiaohongshu.md`](examples/output_xiaohongshu.md) — 带有 Emoji、分段和 #标签 的社交媒体格式。
- **微信公众号输出**: [`examples/output_wechat.md`](examples/output_wechat.md) — 带有 Markdown 排版和引用块的文章格式。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request，特别是添加新的平台适配器！详细贡献流程请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📜 许可证

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2026 Hermes AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**⭐ 如果这个项目对你有帮助，欢迎在 GitHub 上给个 Star！**

[GitHub](https://github.com/JianFeiGan/ai-content-multiplatform) · [PyPI](https://pypi.org/project/ai-content-multiplatform/) · [Issues](https://github.com/JianFeiGan/ai-content-multiplatform/issues)
