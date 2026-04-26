"""内容发布器。"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


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

    def __init__(self, settings: Any, db_path: Optional[str] = None):
        """初始化发布器。

        Args:
            settings: 应用配置
            db_path: 历史数据库路径（None 则使用内存数据库）
        """
        self.settings = settings
        self._db_path = db_path

    @property
    def db_path(self) -> str:
        """获取数据库路径。"""
        return self._db_path or ":memory:"

    def publish(
        self,
        platform: str,
        content_path: Path,
        is_draft: bool = False,
    ) -> PublishResult:
        """发布内容到指定平台。

        Args:
            platform: 平台标识
            content_path: 内容文件路径
            is_draft: 是否草稿模式

        Returns:
            发布结果
        """
        content_path = Path(content_path)
        if not content_path.exists():
            return PublishResult(
                success=False,
                platform=platform,
                error=f"文件不存在: {content_path}",
            )

        if is_draft:
            result = PublishResult(
                success=True,
                platform=platform,
                url="",
                published_at=datetime.now(),
            )
            self._save_history(platform, content_path, result, is_draft=True)
            return result

        # 模拟发布
        content = content_path.read_text(encoding="utf-8")
        result = self._do_publish(platform, content)
        self._save_history(platform, content_path, result, is_draft=False)
        return result

    def publish_batch(
        self,
        items: list[tuple[str, Path]],
        is_draft: bool = False,
    ) -> list[PublishResult]:
        """批量发布内容。

        Args:
            items: (平台, 内容路径) 列表
            is_draft: 是否草稿模式

        Returns:
            发布结果列表
        """
        results = []
        for platform, content_path in items:
            result = self.publish(platform, content_path, is_draft=is_draft)
            results.append(result)
        return results

    def _do_publish(self, platform: str, content: str) -> PublishResult:
        """执行实际发布（模拟）。

        Args:
            platform: 平台标识
            content: 内容文本

        Returns:
            发布结果
        """
        # 模拟发布成功
        return PublishResult(
            success=True,
            platform=platform,
            url=f"https://{platform}.example.com/post/{hash(content) % 10000}",
        )

    def _save_history(
        self,
        platform: str,
        content_path: Path,
        result: PublishResult,
        is_draft: bool = False,
    ) -> None:
        """保存发布历史到 SQLite。

        Args:
            platform: 平台标识
            content_path: 内容文件路径
            result: 发布结果
            is_draft: 是否草稿
        """
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS publish_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    content_path TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    url TEXT,
                    error TEXT,
                    is_draft INTEGER NOT NULL DEFAULT 0,
                    published_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                INSERT INTO publish_history
                (platform, content_path, success, url, error, is_draft, published_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                platform,
                str(content_path),
                1 if result.success else 0,
                result.url,
                result.error,
                1 if is_draft else 0,
                result.published_at.isoformat(),
            ))
            conn.commit()
        finally:
            conn.close()

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """获取发布历史。

        Args:
            limit: 返回条数限制

        Returns:
            历史记录列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.execute(
                "SELECT * FROM publish_history ORDER BY published_at DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
