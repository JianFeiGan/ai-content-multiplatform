"""Formatter 模块测试。"""
from __future__ import annotations

from ai_content_multiplatform.utils.formatter import (
    strip_markdown,
    truncate_text,
    strip_forbidden_words,
)


def test_strip_markdown_bold() -> None:
    """测试移除粗体标记。"""
    assert strip_markdown("**粗体**") == "粗体"


def test_strip_markdown_italic() -> None:
    """测试移除斜体标记。"""
    assert strip_markdown("*斜体*") == "斜体"


def test_strip_markdown_links() -> None:
    """测试链接保留文字。"""
    assert strip_markdown("[文字](http://example.com)") == "文字"


def test_strip_markdown_images() -> None:
    """测试移除图片标记。"""
    assert strip_markdown("前![alt](url)后") == "前后"


def test_strip_markdown_code() -> None:
    """测试移除行内代码。"""
    assert strip_markdown("使用 `code` 示例") == "使用 code 示例"


def test_strip_markdown_headings() -> None:
    """测试移除标题标记。"""
    assert strip_markdown("## 标题") == "标题"


def test_truncate_text_short() -> None:
    """测试短文本不截断。"""
    assert truncate_text("短文本", 10) == "短文本"


def test_truncate_text_long() -> None:
    """测试长文本截断。"""
    text = "这是一段很长的文本"
    result = truncate_text(text, 5)
    assert len(result) == 5
    assert result.endswith("...")


def test_truncate_text_custom_suffix() -> None:
    """测试自定义截断后缀。"""
    result = truncate_text("这是一段长文本", 4, suffix="→")
    assert result.endswith("→")


def test_strip_forbidden_words_empty() -> None:
    """测试无禁用词返回原文。"""
    assert strip_forbidden_words("原文", []) == "原文"


def test_strip_forbidden_words_match() -> None:
    """测试移除禁用词。"""
    result = strip_forbidden_words("这是微信内容", ["微信"])
    assert "微信" not in result
