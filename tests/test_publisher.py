"""Publisher 模块测试。"""
from __future__ import annotations

import pytest

from ai_content_multiplatform.core.publisher import Publisher
from ai_content_multiplatform.core.models import AdaptedContent


def test_publisher_single() -> None:
    """测试单平台发布。"""
    publisher = Publisher()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="测试标题",
        content="测试内容",
        tags=[],
    )

    result = publisher.publish(content, draft=True)
    assert "status" in result
    assert result["status"] == "draft"


def test_publisher_batch() -> None:
    """测试批量发布。"""
    publisher = Publisher()
    contents = [
        AdaptedContent(
            platform=pid,
            platform_name=pid,
            title=f"标题_{pid}",
            content=f"内容_{pid}",
            tags=[],
        )
        for pid in ["weixin", "zhihu"]
    ]

    results = publisher.publish_batch(contents, draft=True)
    assert len(results) == 2


def test_publisher_history() -> None:
    """测试历史记录。"""
    publisher = Publisher()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="历史测试",
        content="内容",
        tags=[],
    )

    publisher.publish(content, draft=False)
    history = publisher.get_history()

    assert len(history) > 0
    assert any(r.get("title") == "历史测试" for r in history)


def test_publisher_draft_mode() -> None:
    """测试草稿模式。"""
    publisher = Publisher()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="草稿测试",
        content="内容",
        tags=[],
    )

    result = publisher.publish(content, draft=True)
    assert result.get("status") == "draft"
