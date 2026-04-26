# 技术方案文档

> **项目名称**：AI Content Multiplatform
> **创建日期**：2026-04-26
> **作者**：Hermes AI
> **版本**：v0.1

---

## 1. 系统架构

### 1.1 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    CLI 入口层                             │
│  ai-content-multiplatform [COMMAND] [OPTIONS]            │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   业务逻辑层                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ 内容解析器   │  │ 适配引擎     │  │ 发布管理器   │   │
│  │ (Parser)    │─▶│ (Adapter)   │─▶│ (Publisher) │   │
│  └─────────────┘  └──────────────┘  └──────────────┘   │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   平台适配层                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────┐  │
│  │微信    │ │知乎    │ │CSDN    │ │抖音    │ │小红书│  │
│  │Adapter │ │Adapter │ │Adapter │ │Adapter │ │Adapter│ │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────┘  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   配置与存储层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 平台配置      │  │ 规则引擎     │  │ 历史记录     │  │
│  │ (YAML/JSON) │  │ (Rules)     │  │ (SQLite)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 1.2 模块划分

| 模块 | 职责 | 依赖 |
|-----|------|-----|
| cli | CLI 命令入口、参数解析 | typer, rich |
| core.parser | 内容解析（Markdown/文本） | markdown, beautifulsoup4 |
| core.adapter | 平台适配引擎、LLM 调用 | openai, pydantic |
| core.publisher | 平台发布管理 | httpx, platform adapters |
| config.settings | 配置管理、平台规则 | pydantic-settings, pyyaml |
| utils.helpers | 工具函数（日志、格式化） | rich, logging |

### 1.3 数据流
1. 用户输入核心内容（Markdown）
2. Parser 解析内容为结构化数据（标题、正文、图片、标签）
3. Adapter 根据平台规则调用 LLM 进行适配
4. Publisher 将适配后的内容发布到各平台（可选）
5. 历史记录保存到本地 SQLite

---

## 2. 技术选型

### 2.1 编程语言
- **选择**：Python 3.11+
- **理由**：AI/LLM 生态最完善，用户群体匹配（开发者/技术博主）

### 2.2 核心框架
| 组件 | 选型 | 替代方案 | 选择理由 |
|-----|------|---------|---------|
| CLI 框架 | typer | click, argparse | 自动类型转换、现代 API |
| LLM 调用 | openai | anthropic, litellm | 生态最成熟、文档完善 |
| 配置管理 | pydantic-settings | dotenv, configparser | 类型安全、验证 |
| 终端输出 | rich | click, colorama | 丰富 UI 组件 |
| HTTP 客户端 | httpx | requests, aiohttp | 异步支持、现代 API |

### 2.3 关键依赖
| 依赖 | 版本 | 用途 |
|-----|------|-----|
| typer | >=0.9.0 | CLI 框架 |
| pydantic | >=2.0.0 | 数据验证 |
| pydantic-settings | >=2.0.0 | 配置管理 |
| rich | >=13.0.0 | 终端美化 |
| httpx | >=0.25.0 | HTTP 客户端 |
| openai | >=1.0.0 | LLM API |
| pyyaml | >=6.0 | 配置文件 |
| markdown | >=3.5 | Markdown 解析 |

---

## 3. API/接口设计

### 3.1 CLI 命令

```
ai-content-multiplatform [COMMAND] [OPTIONS]

Commands:
  init        初始化配置
  adapt       适配内容到多平台
  publish     发布到指定平台
  preview     预览适配效果
  config      管理配置
  history     查看历史记录

Examples:
  ai-content-multiplatform adapt -i article.md -p weixin zhihu csdn
  ai-content-multiplatform preview -i article.md -p weixin
  ai-content-multiplatform publish -i article.md -p weixin --draft
```

### 3.2 核心数据结构

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentInput(BaseModel):
    """输入内容"""
    title: str
    content: str  # Markdown
    tags: list[str] = []
    images: list[str] = []
    author: Optional[str] = None

class PlatformRule(BaseModel):
    """平台规则"""
    platform: str
    title_max_len: int
    content_max_len: int
    tag_limit: int
    cover_size: tuple[int, int]  # width, height
    style_prompt: str  # LLM 风格提示词
    forbidden_words: list[str] = []

class AdaptedContent(BaseModel):
    """适配后的内容"""
    platform: str
    title: str
    content: str
    tags: list[str]
    cover_suggestion: Optional[str] = None
    adapted_at: datetime = datetime.now()
```

---

## 4. 目录结构

```
ai-content-multiplatform/
├── docs/                    # 文档
│   ├── 01-business-requirements.md
│   ├── 02-technical-design.md
│   └── 03-self-review.md
├── src/
│   └── ai_content_multiplatform/
│       ├── __init__.py
│       ├── cli/             # CLI 入口
│       │   ├── __init__.py
│       │   ├── main.py      # typer app
│       │   ├── adapt.py     # adapt 命令
│       │   ├── publish.py   # publish 命令
│       │   └── preview.py   # preview 命令
│       ├── core/            # 核心逻辑
│       │   ├── __init__.py
│       │   ├── parser.py    # 内容解析
│       │   ├── adapter.py   # 适配引擎
│       │   ├── publisher.py # 发布管理
│       │   └── llm.py       # LLM 调用封装
│       ├── platforms/       # 平台适配器
│       │   ├── __init__.py
│       │   ├── base.py      # 基类
│       │   ├── weixin.py    # 微信
│       │   ├── zhihu.py     # 知乎
│       │   ├── csdn.py      # CSDN
│       │   ├── douyin.py    # 抖音
│       │   └── xiaohongshu.py # 小红书
│       ├── config/          # 配置
│       │   ├── __init__.py
│       │   ├── settings.py  # 全局配置
│       │   └── rules.yaml   # 平台规则
│       └── utils/           # 工具
│           ├── __init__.py
│           ├── logger.py    # 日志
│           └── formatter.py # 格式化
├── tests/                   # 测试
│   ├── test_parser.py
│   ├── test_adapter.py
│   ├── test_publisher.py
│   └── conftest.py
├── README.md
├── LICENSE
├── CHANGELOG.md
├── pyproject.toml
└── .github/workflows/
    ├── test.yml
    └── release.yml
```

---

## 5. 测试策略

### 5.1 测试类型
| 类型 | 工具 | 覆盖率目标 | 说明 |
|-----|------|-----------|------|
| 单元测试 | pytest | > 80% | 核心逻辑测试 |
| 集成测试 | pytest | > 60% | LLM 调用、平台适配 |
| CLI 测试 | pytest + typer testing | 关键路径 | 命令解析 |

### 5.2 测试用例设计
- **正常路径**：标准 Markdown 输入 → 多平台适配 → 输出
- **边界条件**：超长内容、特殊字符、空输入
- **异常处理**：LLM 调用失败、网络超时、配置错误

---

## 6. 开发计划

### 6.1 里程碑
| 里程碑 | 日期 | 交付物 | 状态 |
|-------|------|-------|------|
| M1: 项目骨架 | 5 月 4 日 | CLI 框架、配置系统 | 待开始 |
| M2: 解析器 + 适配器 | 5 月 11 日 | Parser、Adapter 核心 | 待开始 |
| M3: 平台规则 + 预览 | 5 月 18 日 | 5 平台规则、预览功能 | 待开始 |
| M4: 发布 + 测试 + 文档 | 5 月 25 日 | 发布功能、测试、文档 | 待开始 |
| M5: 发布上线 | 5 月 31 日 | GitHub Release、PyPI | 待开始 |

---

## 7. 质量标准

### 7.1 代码规范
- [ ] 类型注解覆盖所有公共函数
- [ ] 所有函数有 docstring
- [ ] 遵循 PEP 8 规范
- [ ] 无硬编码配置

### 7.2 性能要求
- [ ] 单平台适配时间 < 30 秒
- [ ] CLI 启动时间 < 2 秒
- [ ] 内存占用 < 200MB

---

*本文档由 Hermes AI 自主设计，技术方案自主审核。*
