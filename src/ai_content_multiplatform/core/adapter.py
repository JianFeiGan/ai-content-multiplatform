"""内容适配器，将原始内容适配到不同平台。"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Optional

from ai_content_multiplatform.core.models import (
    AdaptedContent,
    ContentInput,
    PlatformResult,
    PlatformRule,
)
from ai_content_multiplatform.utils.formatter import truncate_text, strip_forbidden_words


class ContentAdapter:
    """内容适配器。"""

    def __init__(self, settings: Any, llm_client: Any = None):
        """初始化适配器。

        Args:
            settings: 应用配置
            llm_client: LLM 客户端（可选，为 None 时使用规则适配）
        """
        self.settings = settings
        self.llm_client = llm_client

    def adapt(self, content: ContentInput, platform_id: str) -> AdaptedContent:
        """将内容适配到指定平台。

        Args:
            content: 原始内容
            platform_id: 平台标识

        Returns:
            适配后的内容

        Raises:
            ValueError: 平台规则不存在
        """
        rule = self.settings.get_platform_rule(platform_id)
        if rule is None:
            raise ValueError(f"平台规则不存在: {platform_id}")

        # 标题适配
        title = self._adapt_title(content.title, rule)

        # 内容适配
        adapted_content = self._adapt_content(content.content, rule)

        # 标签适配
        tags = self._adapt_tags(content.tags, rule)

        return AdaptedContent(
            platform=platform_id,
            platform_name=rule.name,
            title=title,
            content=adapted_content,
            tags=tags,
        )

    async def adapt_multi(
        self,
        content: ContentInput,
        platform_ids: list[str],
    ) -> PlatformResult:
        """并发适配多个平台。

        Args:
            content: 原始内容
            platform_ids: 平台标识列表

        Returns:
            多平台适配结果
        """
        tasks = []
        for pid in platform_ids:
            tasks.append(self._adapt_async(content, pid))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        adapted_list = []
        for r in results:
            if isinstance(r, Exception):
                continue
            adapted_list.append(r)

        return PlatformResult(
            source_title=content.title,
            source_content=content.content,
            platforms=adapted_list,
        )

    async def _adapt_async(
        self,
        content: ContentInput,
        platform_id: str,
    ) -> AdaptedContent:
        """异步适配单个平台。"""
        return self.adapt(content, platform_id)

    def _adapt_title(self, title: str, rule: PlatformRule) -> str:
        """适配标题（截断 + 过滤禁用词）。"""
        # 先过滤禁用词
        title = strip_forbidden_words(title, rule.forbidden_words)
        # 再截断
        title = truncate_text(title, rule.title_max_len)
        return title.strip()

    def _adapt_content(self, content: str, rule: PlatformRule) -> str:
        """适配内容（截断 + 过滤禁用词）。"""
        # 先过滤禁用词
        content = strip_forbidden_words(content, rule.forbidden_words)
        # 再截断
        content = truncate_text(content, rule.content_max_len)
        return content.strip()

    def _adapt_tags(self, tags: list[str], rule: PlatformRule) -> list[str]:
        """适配标签（数量限制）。"""
        if rule.tag_limit <= 0:
            return []
        return tags[: rule.tag_limit]

    def adapt_with_llm(
        self,
        content: ContentInput,
        platform_id: str,
    ) -> dict[str, Any]:
        """使用 LLM 进行高级适配（需要 llm_client）。

        Args:
            content: 原始内容
            platform_id: 平台标识

        Returns:
            LLM 返回的适配结果字典

        Raises:
            ValueError: llm_client 未设置
        """
        if self.llm_client is None:
            raise ValueError("llm_client 未设置")

        rule = self.settings.get_platform_rule(platform_id)
        if rule is None:
            raise ValueError(f"平台规则不存在: {platform_id}")

        system_prompt = rule.style_prompt
        user_content = json.dumps({
            "title": content.title,
            "content": content.content,
            "tags": content.tags,
        }, ensure_ascii=False)

        # 返回同步调用的适配结果（内部用异步）
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 在已运行的事件循环中创建新任务
                return asyncio.ensure_future(
                    self.llm_client.adapt_content(system_prompt, user_content)
                )
            else:
                return loop.run_until_complete(
                    self.llm_client.adapt_content(system_prompt, user_content)
                )
        except RuntimeError:
            # 没有事件循环
            return asyncio.run(
                self.llm_client.adapt_content(system_prompt, user_content)
            )
