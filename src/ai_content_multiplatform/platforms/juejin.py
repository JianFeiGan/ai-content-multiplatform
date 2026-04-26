"""掘金平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class JuejinPlatformAdapter(BasePlatformAdapter):
    """掘金技术社区平台适配器。

    特点：
    - 支持 Markdown 格式
    - 标题限制 100 字符
    - 支持最多 5 个标签
    - 技术社区，强调技术深度和代码质量
    """

    platform_id = "juejin"
    platform_name = "掘金"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证掘金内容。

        Args:
            content: 待验证的内容。

        Returns:
            验证是否通过。

        Raises:
            ValidationError: 当内容不符合要求时抛出。
        """
        super().validate_content(content)

        if len(content.title) > 100:
            raise ValidationError(
                "掘金标题不能超过 100 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.tags) > 5:
            raise ValidationError(
                "掘金最多支持 5 个标签",
                f"当前数量: {len(content.tags)}",
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到掘金。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成掘金 API
        # - 使用掘金的创作平台 API
        # - 支持 Markdown 格式发布
        # - 需要选择技术分类和标签
        return await self._mock_publish(content, draft)
