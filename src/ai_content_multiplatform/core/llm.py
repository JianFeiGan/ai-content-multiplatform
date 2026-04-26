"""LLM 调用封装 - 基于 OpenAI API 的内容适配。"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Optional

from openai import AsyncOpenAI

from .exceptions import LLMCallError

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


class LLMClient:
    """OpenAI LLM 客户端，支持异步调用和重试。

    Args:
        api_key: OpenAI API Key。
        base_url: API 基础 URL（可选，用于兼容代理）。
        model: 默认模型名称。
        temperature: 默认温度参数。
        max_tokens: 默认最大 token 数。
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> None:
        if not api_key:
            raise LLMCallError("OpenAI API key is required")

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        client_kwargs: dict = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url

        self._client = AsyncOpenAI(**client_kwargs)  # type: ignore[arg-type]

    async def adapt_content(
        self,
        prompt: str,
        system_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """调用 LLM 进行内容适配。

        Args:
            prompt: 用户提示词（包含原始内容和适配要求）。
            system_prompt: 系统提示词（平台风格定义）。
            model: 模型名称（覆盖默认值）。
            temperature: 温度参数（覆盖默认值）。
            max_tokens: 最大 token 数（覆盖默认值）。

        Returns:
            str: LLM 返回的文本响应。

        Raises:
            LLMCallError: API 调用失败时抛出。
        """
        model_name = model or self.model
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens or self.max_tokens

        last_error: Optional[Exception] = None

        for attempt in range(MAX_RETRIES):
            try:
                response = await self._client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temp,
                    max_tokens=tokens,
                )

                content = response.choices[0].message.content
                if not content:
                    raise LLMCallError("LLM returned empty response")

                logger.info("LLM call succeeded on attempt %d", attempt + 1)
                return content

            except Exception as e:
                last_error = e
                logger.warning(
                    "LLM call failed on attempt %d: %s", attempt + 1, e
                )
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY * (2 ** attempt)
                    await asyncio.sleep(delay)

        raise LLMCallError(
            f"LLM call failed after {MAX_RETRIES} attempts: {last_error}"
        )

    async def adapt_content_json(
        self,
        prompt: str,
        system_prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        """调用 LLM 并解析 JSON 响应。

        Args:
            prompt: 用户提示词。
            system_prompt: 系统提示词。
            model: 模型名称。
            temperature: 温度参数。
            max_tokens: 最大 token 数。

        Returns:
            dict: 解析后的 JSON 响应。

        Raises:
            LLMCallError: API 调用失败或 JSON 解析失败时抛出。
        """
        response = await self.adapt_content(
            prompt=prompt,
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # 提取 JSON（可能包含 markdown 代码块标记）
        json_str = response.strip()
        if json_str.startswith("```"):
            json_str = re.sub(r"^```(?:json)?\s*", "", json_str)
            json_str = re.sub(r"\s*```$", "", json_str)

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise LLMCallError(f"Failed to parse LLM JSON response: {e}")

    async def close(self) -> None:
        """关闭客户端连接。"""
        await self._client.close()


import re
