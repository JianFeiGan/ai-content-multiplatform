"""Adapter 模块测试。"""
from __future__ import annotations

import pytest

from ai_content_multiplatform.core.adapter import ContentAdapter
from ai_content_multiplatform.core.models import ContentInput
from ai_content_multiplatform.config.settings import AppConfig


def test_adapter_single_platform(sample_content_input: ContentInput) -> None:
    """测试单平台适配。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    result = adapter.adapt(sample_content_input, "weixin")

    assert result.platform == "weixin"
    assert result.platform_name == "微信公众号"
    assert len(result.title) <= 64


def test_adapter_title_truncation() -> None:
    """测试标题截断。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(
        title="这是一个非常非常非常长的标题用于测试截断功能是否正常工作",
        content="内容",
        tags=[],
    )

    result = adapter.adapt(content, "xiaohongshu")
    assert len(result.title) <= 20


def test_adapter_content_truncation() -> None:
    """测试内容截断。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(
        title="标题",
        content="A" * 2000,
        tags=[],
    )

    result = adapter.adapt(content, "douyin")
    assert len(result.content) <= 300


def test_adapter_forbidden_words() -> None:
    """测试禁用词过滤。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(
        title="微信测试",
        content="这是微信内容",
        tags=[],
    )

    result = adapter.adapt(content, "xiaohongshu")
    assert "微信" not in result.title
    assert "微信" not in result.content


def test_adapter_tag_limit() -> None:
    """测试标签数量限制。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(
        title="标题",
        content="内容",
        tags=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
    )

    result = adapter.adapt(content, "zhihu")
    assert len(result.tags) <= 5


def test_adapter_no_tags_for_weixin() -> None:
    """测试微信公众号不输出标签。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(
        title="标题",
        content="内容",
        tags=["AI", "技术"],
    )

    result = adapter.adapt(content, "weixin")
    assert len(result.tags) == 0


def test_adapter_invalid_platform() -> None:
    """测试无效平台抛出异常。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    content = ContentInput(title="标题", content="内容", tags=[])

    with pytest.raises(ValueError, match="不存在"):
        adapter.adapt(content, "nonexistent_platform")


@pytest.mark.asyncio
async def test_adapter_multi_platform(sample_content_input: ContentInput) -> None:
    """测试多平台并发适配。"""
    settings = AppConfig()
    adapter = ContentAdapter(settings=settings)

    result = await adapter.adapt_multi(
        sample_content_input, ["weixin", "zhihu", "csdn"]
    )

    assert len(result.platforms) == 3
    platforms = {p.platform for p in result.platforms}
    assert platforms == {"weixin", "zhihu", "csdn"}
