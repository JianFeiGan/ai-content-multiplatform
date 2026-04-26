"""Parser 模块测试。"""
from __future__ import annotations

import pytest
from pathlib import Path

from ai_content_multiplatform.core.parser import parse_markdown, parse_file
from ai_content_multiplatform.core.exceptions import ContentParserError


def test_parse_markdown_with_frontmatter(sample_markdown: str) -> None:
    """测试带 YAML front matter 的 Markdown 解析。"""
    result = parse_markdown(sample_markdown)

    assert result.title == "AI 如何改变内容创作"
    assert "AI" in result.tags
    assert result.author == "Hermes"
    assert len(result.images) > 0
    assert "https://example.com/ai-creative.jpg" in result.images


def test_parse_markdown_without_frontmatter() -> None:
    """测试不带 front matter 的解析（从标题提取）。"""
    text = "# 测试标题\n\n这是正文内容。"
    result = parse_markdown(text)

    assert result.title == "测试标题"
    assert "这是正文内容" in result.content


def test_parse_markdown_auto_title() -> None:
    """测试无标题时自动提取前50字符。"""
    text = "这是一段很长的内容，用于测试自动标题提取功能是否正常工作。"
    result = parse_markdown(text)

    assert len(result.title) <= 53  # 50 + "..."


def test_parse_markdown_empty() -> None:
    """测试空内容抛出异常。"""
    with pytest.raises(ContentParserError, match="empty"):
        parse_markdown("")

    with pytest.raises(ContentParserError, match="empty"):
        parse_markdown("   ")


def test_parse_file(tmp_path: Path) -> None:
    """测试从文件解析。"""
    test_file = tmp_path / "test.md"
    test_file.write_text("# 文件测试\n\n内容", encoding="utf-8")

    result = parse_file(str(test_file))
    assert result.title == "文件测试"


def test_parse_file_not_found() -> None:
    """测试文件不存在时抛出异常。"""
    with pytest.raises(ContentParserError, match="not found"):
        parse_file("/nonexistent/file.md")


def test_parse_markdown_tags_from_content() -> None:
    """测试从正文提取标签。"""
    text = "# 标题\n\n这是关于 #Python 和 #AI 的内容"
    result = parse_markdown(text)

    assert "Python" in result.tags
    assert "AI" in result.tags
