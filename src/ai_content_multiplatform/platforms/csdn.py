"""CSDN 平台适配器。"""

from __future__ import annotations

from typing import Any

from ai_content_multiplatform.core.exceptions import ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.platforms.base import BasePlatformAdapter


class CSDNPlatformAdapter(BasePlatformAdapter):
    """CSDN 平台适配器。

    特点：
    - 支持 Markdown 格式
    - 标题限制 100 字符
    - 支持最多 10 个标签
    - 技术博客平台，代码块需指定语言
    """

    platform_id = "csdn"
    platform_name = "CSDN"

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证 CSDN 内容。

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
                "CSDN 标题不能超过 100 字符",
                f"当前长度: {len(content.title)}",
            )

        if len(content.tags) > 10:
            raise ValidationError(
                "CSDN 最多支持 10 个标签",
                f"当前数量: {len(content.tags)}",
            )

        # 检查代码块是否指定语言
        import re

        unspecified = re.findall(r"```\s*\n", content.content)
        if unspecified:
            self._logger.warning(
                f"发现 {len(unspecified)} 个未指定语言的代码块，"
                "建议为代码块指定编程语言"
            )

        return True

    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到 CSDN。

        Args:
            content: 适配后的内容。
            draft: 是否保存为草稿。

        Returns:
            发布结果字典。
        """
        self.validate_content(content)

        # TODO: 集成 CSDN API
        # - CSDN 提供 Markdown 编辑器接口
        # - 使用 Cookie 或 API Key 认证
        # - 调用文章发布接口
        return await self._mock_publish(content, draft)
