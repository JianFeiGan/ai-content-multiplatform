"""内容解析器 - 解析 Markdown 内容为结构化数据。"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .models import ContentInput
from .exceptions import ContentParserError

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


def _extract_frontmatter(text: str) -> tuple[dict, str]:
    """提取 YAML front matter，返回 (metadata, remaining_text)。"""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    raw = match.group(1)
    if yaml is None:
        raise ContentParserError("PyYAML is required for front matter parsing")

    metadata = yaml.safe_load(raw) or {}
    remaining = match.group(2)
    return metadata, remaining


def parse_markdown(text: str) -> ContentInput:
    """解析 Markdown 文本为 ContentInput。

    支持从 YAML front matter 提取 title, tags, author 元数据。
    若无 front matter，则从正文第一行提取标题（首个 # 标题）。

    Args:
        text: Markdown 格式的文本内容。

    Returns:
        ContentInput: 结构化的内容对象。

    Raises:
        ContentParserError: 内容为空或解析失败时抛出。
    """
    if not text or not text.strip():
        raise ContentParserError("Content is empty")

    metadata, body = _extract_frontmatter(text.strip())

    title: Optional[str] = metadata.get("title")
    tags: list[str] = metadata.get("tags", [])
    author: Optional[str] = metadata.get("author")

    # 如果没有 front matter 标题，从正文提取
    if not title:
        title_match = re.match(r"^#\s+(.+)$", body, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # 移除提取的标题行
            body = re.sub(r"^#\s+.+$\n?", "", body, count=1, flags=re.MULTILINE)
        else:
            # 用正文前50字符作为标题
            title = body.strip()[:50] + ("..." if len(body.strip()) > 50 else "")

    # 提取正文中的图片
    images = re.findall(r"!\[.*?\]\(([^)]+)\)", body)

    # 如果没有 tags，尝试从正文提取标签
    if not tags:
        tag_matches = re.findall(r"#(\S+)", body)
        tags = tag_matches[:10]

    return ContentInput(
        title=title,
        content=body.strip(),
        tags=tags,
        images=images,
        author=author,
    )


def parse_file(filepath: str) -> ContentInput:
    """从文件读取并解析 Markdown 内容。

    Args:
        filepath: Markdown 文件路径。

    Returns:
        ContentInput: 结构化的内容对象。

    Raises:
        ContentParserError: 文件不存在或解析失败时抛出。
    """
    path = Path(filepath)
    if not path.exists():
        raise ContentParserError(f"File not found: {filepath}")
    if not path.is_file():
        raise ContentParserError(f"Not a file: {filepath}")

    text = path.read_text(encoding="utf-8")
    return parse_markdown(text)
