"""头条号平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class ToutiaoPlatformAdapter(BasePlatformAdapter):
    """头条号平台适配器。

    特点：
    - 标题限制 30 字符
    - 支持最多 5 个标签
    - 资讯平台风格，通俗化表达
    - 支持三图封面模式
    """

    platform_id = "toutiao"
    platform_name = "头条号"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证头条号内容。

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
                "头条号标题不能超过 30 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.tags) > 5:
            raise ValidationError(
                "头条号最多支持 5 个标签",
                f"当前数量: {len(content.tags)}",
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到头条号。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成头条号开放平台 API
        # - 使用头条号开放平台的图文发布接口
        # - 支持三图封面、单图封面、无图模式
        # - 需要选择分类和标签
        return await self._mock_publish(content, draft)
