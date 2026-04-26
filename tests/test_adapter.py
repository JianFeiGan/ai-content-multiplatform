"""Adapter 模块测试。"""
from __future__ import annotations

import pytest
from unittest.mock import Mock, AsyncMock

from ai_content_multiplatform.core.adapter import ContentAdapter
from ai_content_multiplatform.core.models import ContentInput, PlatformRule

@pytest.fixture
def mock_settings():
    settings = Mock()
    settings.get_platform_rule.return_value = PlatformRule(
        name="Test", title_max_len=20, content_max_len=50, 
        tag_limit=3, forbidden_words=[], style_prompt="Test style", cover_size=(1, 1)
    )
    return settings

@pytest.fixture
def content():
    return ContentInput(
        title="A very long title that should be truncated eventually",
        content="Short content.",
        tags=["tag1", "tag2", "tag3", "tag4", "tag5"]
    )

def test_adapt_single(mock_settings, content):
    adapter = ContentAdapter(settings=mock_settings)
    result = adapter.adapt(content, "test_platform")
    assert result.platform == "test_platform"
    assert len(result.title) <= 20
    assert len(result.tags) <= 3

@pytest.mark.asyncio
async def test_adapt_with_llm(mock_settings, content):
    mock_llm = Mock()
    mock_llm.adapt_content_json = AsyncMock(return_value={
        "title": "New Title",
        "content": "New Content",
        "tags": ["a", "b"]
    })
    
    adapter = ContentAdapter(settings=mock_settings, llm_client=mock_llm)
    result = await adapter.adapt_with_llm_async(content, "test_platform")
    
    assert result.title == "New Title"
    assert result.content == "New Content"
    assert len(result.tags) == 2
