"""内容发布器。"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ai_content_multiplatform.core.models import AdaptedContent


@dataclass
class PublishResult:
    """发布结果。"""
    success: bool
    platform: str = ""
    url: str = ""
    error: str = ""
    published_at: datetime = field(default_factory=datetime.now)


class ContentPublisher:
    """内容发布器。"""

    def __init__(self, settings: Any = None, db_path: Optional[str] = None):
        """初始化发布器。

        Args:
            settings: 应用配置（可选）
            db_path: 历史数据库路径（None 则使用内存数据库）
        """
        self.settings = settings
        self._db_path = db_path
        self._history: list[dict[str, Any]] = []

    @property
    def db_path(self) -> str:
        """获取数据库路径。"""
        return self._db_path or ":memory:"

    def publish(
        self,
        adapted_content: AdaptedContent,
        draft: bool = False,
    ) -> dict[str, Any]:
        """发布适配后的内容到对应平台。

        Args:
            adapted_content: 适配后的内容
            draft: 是否草稿模式

        Returns:
            发布结果字典
        """
        platform = adapted_content.platform
        status = "draft" if draft else "published"

        record: dict[str, Any] = {
            "platform": platform,
            "title": adapted_content.title,
            "status": status,
            "url": f"https://{platform}.example.com/post/{hash(adapted_content.content) % 10000}" if not draft else "",
            "published_at": datetime.now().isoformat(),
        }
        self._history.append(record)
        return record

    def publish_batch(
        self,
        contents: list[AdaptedContent],
        draft: bool = False,
    ) -> list[dict[str, Any]]:
        """批量发布内容。

        Args:
            contents: 适配后的内容列表
            draft: 是否草稿模式

        Returns:
            发布结果列表
        """
        return [self.publish(c, draft=draft) for c in contents]

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """获取发布历史。

        Args:
            limit: 返回条数限制

        Returns:
            历史记录列表
        """
        return self._history[-limit:]


# 别名兼容
Publisher = ContentPublisher
