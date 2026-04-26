"""抖音平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class DouyinPlatformAdapter(BasePlatformAdapter):
    """抖音平台适配器。

    特点：
    - 短视频平台，内容为口播文案/脚本
    - 标题限制 30 字符
    - 内容限制 300 字符
    - 支持最多 15 个标签（话题）
    """

    platform_id = "douyin"
    platform_name = "抖音"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证抖音内容。

        Args:
            content: 待验证的内容。

        Returns:
            验证是否通过。

        Raises:
            ValidationError: 当内容不符合要求时抛出。
        """
        super().validate_content(content)

        if len(content.title) > 30:
            raise ValidationError(
                "抖音标题不能超过 30 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.content) > 300:
            raise ValidationError(
                "抖音内容不能超过 300 字符",
                f"当前长度: {len(content.content)}",
            )

        if len(content.tags) > 15:
            raise ValidationError(
                "抖音最多支持 15 个话题标签",
                f"当前数量: {len(content.tags)}",
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到抖音。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成抖音开放平台 API
        # - 视频内容需要额外处理（此处为文案适配）
        # - 使用抖音开放平台的视频发布接口
        # - 支持话题标签 (@ 话题)
        return await self._mock_publish(content, draft)
