"""Platforms 模块测试。"""
from __future__ import annotations

import pytest

from ai_content_multiplatform.platforms.base import BasePlatformAdapter
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.core.exceptions import ValidationError


def test_base_platform_adapter_abstract() -> None:
    """测试基类是抽象类。"""
    with pytest.raises(TypeError):
        BasePlatformAdapter()


def test_weixin_adapter_validation(weixin_rule) -> None:
    """测试微信公众号适配器验证。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="正常标题",
        content="内容",
        tags=[],
    )

    assert adapter.validate_content(content) is True


def test_weixin_adapter_long_title(weixin_rule) -> None:
    """测试微信公众号超长标题。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="A" * 65,
        content="内容",
        tags=[],
    )

    with pytest.raises(ValidationError, match="64"):
        adapter.validate_content(content)


def test_xiaohongshu_adapter_validation() -> None:
    """测试小红书适配器验证。"""
    from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter

    adapter = XiaohongshuPlatformAdapter()
    content = AdaptedContent(
        platform="xiaohongshu",
        platform_name="小红书",
        title="正常标题",
        content="内容",
        tags=[],
    )

    assert adapter.validate_content(content) is True


def test_douyin_adapter_content_limit() -> None:
    """测试抖音内容限制验证。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="标题",
        content="A" * 301,
        tags=[],
    )

    with pytest.raises(ValidationError):
        adapter.validate_content(content)


@pytest.mark.asyncio
async def test_weixin_publish_mock() -> None:
    """测试微信公众号发布（模拟）。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="测试标题",
        content="测试内容",
        tags=[],
    )

    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result
