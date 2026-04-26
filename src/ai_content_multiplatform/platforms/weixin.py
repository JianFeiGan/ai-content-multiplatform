"""微信公众号平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter
from ai_content_multiplatform.utils.formatter import strip_markdown


class WeixinPlatformAdapter(BasePlatformAdapter):
    """微信公众号平台适配器。

    特点：
    - 不支持原生 Markdown，需转换为纯文本或 HTML
    - 标题限制 64 字符
    - 支持封面图 (900x383)
    """

    platform_id = "weixin"
    platform_name = "微信公众号"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证微信公众号内容。

        Args:
            content: 待验证的内容。

        Returns:
            验证是否通过。

        Raises:
            ValidationError: 当内容不符合要求时抛出。
        """
        super().validate_content(content)

        if len(content.title) > 64:
            raise ValidationError(
                "微信公众号标题不能超过 64 字符",
                f"当前长度: {len(content.title)}",
            )

        # 检查是否包含 Markdown 标记（微信公众号不支持）
        if any(marker in content.content for marker in ["```", "**", "##"]):
            # 自动清理
            content.content = strip_markdown(content.content)

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到微信公众号。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        # 验证并预处理内容
        self.validate_content(content)

        # 确保内容为纯文本格式
        content.content = strip_markdown(content.content)

        # TODO: 集成微信公众号 API
        # - 使用 access_token 调用素材上传接口
        # - 调用草稿箱接口或群发接口
        return await self._mock_publish(content, draft)
