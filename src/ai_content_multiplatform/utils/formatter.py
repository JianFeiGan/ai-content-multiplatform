"""内容格式化工具。"""

from __future__ import annotations

import re


def strip_markdown(text: str) -> str:
    """移除 Markdown 格式标记，保留纯文本。"""
    # 移除图片
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # 链接保留文字
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    # 移除粗体/斜体
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)
    # 移除代码块标记
    text = re.sub(r"```[a-z]*\n", "", text)
    text = re.sub(r"```", "", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    # 移除标题标记
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    # 移除分割线
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    return text.strip()


def truncate_text(text: str, max_len: int, suffix: str = "...") -> str:
    """截断文本到指定长度。"""
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def strip_forbidden_words(text: str, words: list[str]) -> str:
    """移除禁用词。"""
    for word in words:
        text = text.replace(word, "")
    return text
