"""LLM 客户端模块测试 - 使用 mock 测试 LLM 调用逻辑。"""

from __future__ import annotations

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from ai_content_multiplatform.core.llm import LLMClient, MAX_RETRIES, RETRY_DELAY
from ai_content_multiplatform.core.exceptions import LLMCallError


class TestLLMClientInit:
    """测试 LLM 客户端初始化。"""

    def test_init_requires_api_key(self) -> None:
        """测试缺少 API Key 抛出异常。"""
        with pytest.raises(LLMCallError, match="API key"):
            LLMClient(api_key="")

    def test_init_with_api_key(self) -> None:
        """测试正常初始化。"""
        client = LLMClient(api_key="test-key")
        assert client.model == "gpt-4o-mini"
        assert client.temperature == 0.7
        assert client.max_tokens == 4000

    def test_init_with_custom_params(self) -> None:
        """测试自定义参数初始化。"""
        client = LLMClient(
            api_key="test-key",
            base_url="https://api.custom.com/v1",
            model="gpt-4",
            temperature=0.5,
            max_tokens=2000,
        )
        assert client.model == "gpt-4"
        assert client.temperature == 0.5
        assert client.max_tokens == 2000

    def test_init_with_whitespace_key(self) -> None:
        """测试仅空白字符的 API Key 能初始化（验证留给 API 调用时）。"""
        # 空白字符串被 openai SDK 接受，不在此处验证
        client = LLMClient(api_key="  ")
        assert client.model == "gpt-4o-mini"


class TestLLMClientAdapt:
    """测试 LLM 内容适配。"""

    @pytest.mark.asyncio
    async def test_adapt_content_success(self) -> None:
        """测试 LLM 适配成功。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = json.dumps({
            "title": "适配后的标题",
            "content": "适配后的内容",
            "tags": ["AI", "技术"],
            "title_candidates": ["候选1", "候选2"],
        })
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await client.adapt_content(
                prompt="请适配以下内容",
                system_prompt="你是微信公众号编辑",
            )
            # 结果是 JSON 格式，包含 title 字段
            assert "title" in result or "标题" in result

    @pytest.mark.asyncio
    async def test_adapt_content_with_model_override(self) -> None:
        """测试覆盖模型参数。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "简单结果"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_create:
            await client.adapt_content(
                prompt="测试",
                system_prompt="系统提示",
                model="gpt-4",
            )
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs.get("model") == "gpt-4"

    @pytest.mark.asyncio
    async def test_adapt_content_with_temperature_override(self) -> None:
        """测试覆盖温度参数。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "结果"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ) as mock_create:
            await client.adapt_content(
                prompt="测试",
                system_prompt="系统提示",
                temperature=0.3,
            )
            call_kwargs = mock_create.call_args[1]
            assert call_kwargs.get("temperature") == 0.3

    @pytest.mark.asyncio
    async def test_adapt_content_empty_response(self) -> None:
        """测试 LLM 返回空响应。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = None
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ), patch("ai_content_multiplatform.core.llm.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(LLMCallError, match="failed"):
                await client.adapt_content(
                    prompt="测试",
                    system_prompt="系统提示",
                )


class TestLLMClientAdaptJson:
    """测试 JSON 模式的 LLM 适配。"""

    @pytest.mark.asyncio
    async def test_adapt_content_json_success(self) -> None:
        """测试 JSON 适配成功。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = json.dumps({
            "title": "适配标题",
            "content": "适配内容",
            "tags": ["AI"],
        })
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await client.adapt_content_json(
                prompt="请适配",
                system_prompt="你是编辑",
            )
            assert isinstance(result, dict)
            assert result["title"] == "适配标题"

    @pytest.mark.asyncio
    async def test_adapt_content_json_with_code_block(self) -> None:
        """测试 LLM 返回带 markdown 代码块标记的 JSON。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = '```json\n{"title": "标题", "content": "内容"}\n```'
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            result = await client.adapt_content_json(
                prompt="请适配",
                system_prompt="你是编辑",
            )
            assert isinstance(result, dict)
            assert result["title"] == "标题"

    @pytest.mark.asyncio
    async def test_adapt_content_json_parse_error(self) -> None:
        """测试 JSON 解析失败。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "这不是有效的JSON"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            return_value=mock_response,
        ):
            with pytest.raises(LLMCallError, match="JSON"):
                await client.adapt_content_json(
                    prompt="请适配",
                    system_prompt="你是编辑",
                )


class TestLLMClientRetry:
    """测试重试机制。"""

    @pytest.mark.asyncio
    async def test_retry_on_failure_then_success(self) -> None:
        """测试失败后重试成功。"""
        client = LLMClient(api_key="test-key")

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "重试后成功"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]

        call_count = 0

        async def side_effect(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("临时错误")
            return mock_response

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=side_effect,
        ), patch("ai_content_multiplatform.core.llm.asyncio.sleep", new_callable=AsyncMock):
            result = await client.adapt_content(
                prompt="测试",
                system_prompt="系统提示",
            )
            assert result == "重试后成功"
            assert call_count == 2

    @pytest.mark.asyncio
    async def test_retry_max_attempts_exceeded(self) -> None:
        """测试超过最大重试次数。"""
        client = LLMClient(api_key="test-key")

        with patch.object(
            client._client.chat.completions,
            "create",
            new_callable=AsyncMock,
            side_effect=Exception("持续失败"),
        ), patch("ai_content_multiplatform.core.llm.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(LLMCallError, match=f"failed after {MAX_RETRIES}"):
                await client.adapt_content(
                    prompt="测试",
                    system_prompt="系统提示",
                )


class TestLLMClientClose:
    """测试关闭连接。"""

    @pytest.mark.asyncio
    async def test_close(self) -> None:
        """测试关闭客户端连接。"""
        client = LLMClient(api_key="test-key")

        with patch.object(
            client._client, "close", new_callable=AsyncMock
        ):
            await client.close()
