"""内容适配器，将原始内容适配到不同平台。"""

from __future__ import annotations

import json
from typing import Any, Optional

from ai_content_multiplatform.core.models import (
    AdaptedContent,
    ContentInput,
    PlatformRule,
)
from ai_content_multiplatform.utils.formatter import truncate_text, strip_forbidden_words

class ContentAdapter:
    """内容适配器。"""

    def __init__(self, settings: Any, llm_client: Any = None):
        """初始化适配器。"""
        self.settings = settings
        self.llm_client = llm_client

    def adapt(self, content: ContentInput, platform_id: str) -> AdaptedContent:
        """规则适配（截断 + 过滤）。"""
        rule = self.settings.get_platform_rule(platform_id)
        if rule is None:
            raise ValueError(f"平台规则不存在: {platform_id}")

        title = self._adapt_title(content.title, rule)
        adapted_content = self._adapt_content(content.content, rule)
        tags = self._adapt_tags(content.tags, rule)

        return AdaptedContent(
            platform=platform_id,
            platform_name=rule.name,
            title=title,
            content=adapted_content,
            tags=tags,
        )

    async def adapt_with_llm_async(self, content: ContentInput, platform_id: str) -> AdaptedContent:
        """异步 LLM 智能适配。"""
        if self.llm_client is None:
            raise ValueError("llm_client 未设置")

        rule = self.settings.get_platform_rule(platform_id)
        if rule is None:
            raise ValueError(f"平台规则不存在: {platform_id}")

        prompt = (
            f"请作为一名{rule.name}的资深内容创作者，将以下内容适配为该平台风格。"
            "\n要求："
            f"\n1. 标题吸引人，符合{rule.name}风格，长度不超过{rule.title_max_len}。"
            f"\n2. 正文风格：{rule.style_prompt}"
            f"\n3. 标签数量不超过{rule.tag_limit}。"
            '\n4. 请返回 JSON 格式：{"title": "...", "content": "...", "tags": [...]}'
            f"\n\n原始内容：\n{content.content}"
        )

        try:
            result = await self.llm_client.adapt_content_json(
                prompt=prompt,
                system_prompt=f"你是一个专业的{rule.name}内容助手。"
            )
            return AdaptedContent(
                platform=platform_id,
                platform_name=rule.name,
                title=result.get("title", content.title),
                content=result.get("content", content.content),
                tags=result.get("tags", content.tags),
            )
        except Exception as e:
            print(f"LLM 适配失败，降级为规则适配: {e}")
            return self.adapt(content, platform_id)

    def _adapt_title(self, title: str, rule: PlatformRule) -> str:
        title = strip_forbidden_words(title, rule.forbidden_words)
        return truncate_text(title, rule.title_max_len).strip()

    def _adapt_content(self, content: str, rule: PlatformRule) -> str:
        content = strip_forbidden_words(content, rule.forbidden_words)
        return truncate_text(content, rule.content_max_len).strip()

    def _adapt_tags(self, tags: list[str], rule: PlatformRule) -> list[str]:
        if rule.tag_limit <= 0:
            return []
        return tags[: rule.tag_limit]
