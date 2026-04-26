"""平台适配器基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai_content_multiplatform.core.exceptions import PlatformError, ValidationError
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.utils.logger import get_logger

logger = get_logger(__name__)


class BasePlatformAdapter(ABC):
    """平台适配器抽象基类。

    所有平台适配器必须继承此类并实现核心方法。

    Attributes:
        platform_id: 平台标识（如 weixin, zhihu）。
        platform_name: 平台中文名。
    """

    platform_id: str = "base"
    platform_name: str = "基础平台"

    def __init__(self) -> None:
        """初始化平台适配器。"""
        self._logger = get_logger(f"{__name__}.{self.platform_id}")

    @abstractmethod
    async def publish(self, content: AdaptedContent, draft: bool = False) -> dict[str, Any]:
        """发布内容到平台。

        Args:
            content: 适配后的内容。
            draft: 是否作为草稿发布。

        Returns:
            发布结果字典。

        Raises:
            PlatformError: 当发布失败时抛出。
        """

    def get_platform_info(self) -> dict[str, Any]:
        """获取平台基本信息。

        Returns:
            平台信息字典。
        """
        return {
            "platform_id": self.platform_id,
            "platform_name": self.platform_name,
        }

    def validate_content(self, content: AdaptedContent) -> bool:
        """验证内容是否符合平台要求。

        子类可以覆盖此方法以实现平台特定的验证逻辑。

        Args:
            content: 待验证的内容。

        Returns:
            验证是否通过。

        Raises:
            ValidationError: 当内容不符合要求时抛出。
        """
        if not content.title:
            raise ValidationError("标题不能为空", f"平台: {self.platform_name}")
        if not content.content:
            raise ValidationError("内容不能为空", f"平台: {self.platform_name}")
        return True

    async def _mock_publish(
        self,
        content: AdaptedContent,
        draft: bool,
    ) -> dict[str, Any]:
        """模拟发布实现（子类可在正式实现前使用）。

        Args:
            content: 适配后的内容。
            draft: 是否为草稿。

        Returns:
            模拟发布结果。
        """
        import asyncio

        await asyncio.sleep(0.05)  # 模拟网络延迟
        self._logger.info(
            f"[模拟] 发布到 {self.platform_name}: "
            f"标题={content.title}, draft={draft}"
        )
        return {
            "status": "success",
            "platform": self.platform_id,
            "platform_name": self.platform_name,
            "title": content.title,
            "draft": draft,
            "message": f"已{ '保存为草稿' if draft else '发布' }到 {self.platform_name}",
        }
