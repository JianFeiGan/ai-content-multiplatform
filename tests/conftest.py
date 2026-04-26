"""测试 fixtures。"""
from __future__ import annotations

import pytest

from ai_content_multiplatform.core.models import ContentInput, PlatformRule


@pytest.fixture
def sample_markdown() -> str:
    """标准测试用 Markdown 内容。"""
    return """---
title: "AI 如何改变内容创作"
tags: ["AI", "内容创作", "自动化"]
author: "Hermes"
---

# AI 如何改变内容创作

人工智能正在**彻底改变**内容创作的方式。

## 核心优势

1. **效率提升**：AI 可以在几分钟内生成初稿
2. **多平台适配**：自动调整风格适配不同平台
3. **持续优化**：基于数据反馈不断改进

## 代码示例

```python
from ai_content import adapt

result = adapt("AI趋势", platforms=["weixin", "zhihu"])
```

![AI 创作](https://example.com/ai-creative.jpg)

更多内容请关注 #AI #内容创作 #自动化
"""


@pytest.fixture
def sample_content_input() -> ContentInput:
    """标准 ContentInput 实例。"""
    return ContentInput(
        title="AI 如何改变内容创作",
        content="人工智能正在改变内容创作。\n\n## 核心优势\n\n1. 效率提升\n2. 多平台适配",
        tags=["AI", "内容创作"],
        images=["https://example.com/ai.jpg"],
        author="Hermes",
    )


@pytest.fixture
def sample_platform_rules() -> dict[str, PlatformRule]:
    """平台规则字典。"""
    from ai_content_multiplatform.config.settings import AppConfig

    settings = AppConfig()
    return settings.get_platform_rules()


@pytest.fixture
def weixin_rule() -> PlatformRule:
    """微信公众号规则。"""
    return PlatformRule(
        name="微信公众号",
        title_max_len=64,
        content_max_len=20000,
        tag_limit=0,
        cover_size=(900, 383),
        style_prompt="微信公众号风格",
        forbidden_words=["微信", "朋友圈"],
    )


@pytest.fixture
def xiaohongshu_rule() -> PlatformRule:
    """小红书规则。"""
    return PlatformRule(
        name="小红书",
        title_max_len=20,
        content_max_len=1000,
        tag_limit=10,
        cover_size=(1242, 1660),
        style_prompt="小红书风格",
        forbidden_words=["微信", "淘宝"],
    )


@pytest.fixture
def mock_llm_response() -> str:
    """模拟 LLM JSON 响应。"""
    return '{"title": "AI内容创作指南", "content": "适配后的内容...", "tags": ["AI", "创作"], "cover_suggestion": "一张 AI 生成的图片"}'
