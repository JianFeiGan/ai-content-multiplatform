"""知乎平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class ZhihuPlatformAdapter(BasePlatformAdapter):
    """知乎平台适配器。

    特点：
    - 支持 Markdown 格式
    - 标题限制 100 字符
    - 支持最多 5 个标签
    - 适合深度长文
    """

    platform_id = "zhihu"
    platform_name = "知乎"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证知乎内容。

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
                "知乎标题不能超过 100 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.tags) > 5:
            raise ValidationError(
                "知乎最多支持 5 个标签",
                f"当前数量: {len(content.tags)}",
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到知乎。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成知乎 API
        # - 使用 OAuth 获取 access_token
        # - 调用文章创建接口
        # - 支持 Markdown 格式
        return await self._mock_publish(content, draft)
