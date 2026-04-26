"""小红书平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class XiaohongshuPlatformAdapter(BasePlatformAdapter):
    """小红书平台适配器。

    特点：
    - 标题限制 20 字符（非常严格）
    - 内容限制 1000 字符
    - 支持最多 10 个标签
    - 风格轻松活泼，多用 emoji
    """

    platform_id = "xiaohongshu"
    platform_name = "小红书"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证小红书内容。

        Args:
            content: 待验证的内容。

        Returns:
            验证是否通过。

        Raises:
            ValidationError: 当内容不符合要求时抛出。
        """
        super().validate_content(content)

        if len(content.title) > 20:
            raise ValidationError(
                "小红书标题不能超过 20 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.content) > 1000:
            raise ValidationError(
                "小红书内容不能超过 1000 字符",
                f"当前长度: {len(content.content)}",
            )

        if len(content.tags) > 10:
            raise ValidationError(
                "小红书最多支持 10 个标签",
                f"当前数量: {len(content.tags)}",
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到小红书。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成小红书 API
        # - 小红书笔记发布需要图片/视频
        # - 使用蒲公英平台 API
        # - 注意标题字数限制非常严格
        return await self._mock_publish(content, draft)
