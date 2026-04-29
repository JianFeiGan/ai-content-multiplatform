"""内容适配历史记录追踪模块。

提供 SQLite 持久化的适配记录存储，支持：
- 保存每次适配操作的结果
- 按平台、日期、标题查询历史
- 统计各平台适配次数和成功率
- 导出历史记录
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.utils.logger import get_logger

logger = get_logger(__name__)

# 默认数据库路径
DEFAULT_DB_PATH = "~/.ai-content-multiplatform/history.db"


class AdaptHistory:
    """适配历史记录管理器。

    使用 SQLite 存储每次内容适配的操作记录。

    Args:
        db_path: 数据库文件路径。默认为 ~/.ai-content-multiplatform/history.db

    Examples:
        >>> history = AdaptHistory()
        >>> history.save(adapted_content, source_title="原始标题")
        >>> records = history.list_recent(limit=10)
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db_path = Path(db_path or DEFAULT_DB_PATH).expanduser()
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        """获取数据库连接。"""
        if self._conn is None:
            self._conn = sqlite3.connect(str(self._db_path))
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
        return self._conn

    def _init_db(self) -> None:
        """初始化数据库表结构。"""
        conn = self._get_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS adapt_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_title TEXT NOT NULL,
                platform TEXT NOT NULL,
                platform_name TEXT NOT NULL,
                adapted_title TEXT NOT NULL,
                adapted_content TEXT NOT NULL,
                tags TEXT NOT NULL DEFAULT '[]',
                title_candidates TEXT NOT NULL DEFAULT '[]',
                cover_suggestion TEXT,
                adapted_at TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                metadata TEXT NOT NULL DEFAULT '{}'
            );

            CREATE INDEX IF NOT EXISTS idx_platform ON adapt_records(platform);
            CREATE INDEX IF NOT EXISTS idx_adapted_at ON adapt_records(adapted_at);
            CREATE INDEX IF NOT EXISTS idx_source_title ON adapt_records(source_title);
        """)
        conn.commit()

    def save(
        self,
        adapted: AdaptedContent,
        source_title: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> int:
        """保存一条适配记录。

        Args:
            adapted: 适配后的内容对象。
            source_title: 原始内容标题。
            metadata: 附加元数据（如 LLM 模型、耗时等）。

        Returns:
            记录 ID。
        """
        conn = self._get_conn()
        cursor = conn.execute(
            """
            INSERT INTO adapt_records
                (source_title, platform, platform_name, adapted_title,
                 adapted_content, tags, title_candidates, cover_suggestion,
                 adapted_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                source_title or adapted.title,
                adapted.platform,
                adapted.platform_name,
                adapted.title,
                adapted.content,
                json.dumps(adapted.tags, ensure_ascii=False),
                json.dumps(adapted.title_candidates, ensure_ascii=False),
                adapted.cover_suggestion,
                adapted.adapted_at.isoformat(),
                json.dumps(metadata or {}, ensure_ascii=False),
            ),
        )
        conn.commit()
        record_id = cursor.lastrowid
        logger.info(
            f"已保存适配记录 #{record_id}："
            f"{adapted.platform_name} - {adapted.title[:30]}..."
        )
        return record_id

    def save_batch(
        self,
        adapted_list: list[AdaptedContent],
        source_title: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> list[int]:
        """批量保存适配记录。

        Args:
            adapted_list: 适配后的内容列表。
            source_title: 原始内容标题。
            metadata: 附加元数据。

        Returns:
            记录 ID 列表。
        """
        ids = []
        for adapted in adapted_list:
            record_id = self.save(adapted, source_title=source_title, metadata=metadata)
            ids.append(record_id)
        logger.info(f"批量保存了 {len(ids)} 条适配记录")
        return ids

    def list_recent(
        self,
        limit: int = 20,
        platform: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """查询最近的适配记录。

        Args:
            limit: 返回记录数量上限。
            platform: 按平台筛选（可选）。

        Returns:
            记录字典列表。
        """
        conn = self._get_conn()
        if platform:
            rows = conn.execute(
                """
                SELECT * FROM adapt_records
                WHERE platform = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (platform, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM adapt_records
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def get_by_date_range(
        self,
        start_date: str,
        end_date: str,
        platform: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """按日期范围查询适配记录。

        Args:
            start_date: 起始日期 (YYYY-MM-DD)。
            end_date: 结束日期 (YYYY-MM-DD)。
            platform: 按平台筛选（可选）。

        Returns:
            记录字典列表。
        """
        conn = self._get_conn()
        start_dt = f"{start_date}T00:00:00"
        end_dt = f"{end_date}T23:59:59"

        if platform:
            rows = conn.execute(
                """
                SELECT * FROM adapt_records
                WHERE adapted_at BETWEEN ? AND ? AND platform = ?
                ORDER BY adapted_at DESC
                """,
                (start_dt, end_dt, platform),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT * FROM adapt_records
                WHERE adapted_at BETWEEN ? AND ?
                ORDER BY adapted_at DESC
                """,
                (start_dt, end_dt),
            ).fetchall()

        return [self._row_to_dict(row) for row in rows]

    def search(
        self,
        keyword: str,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        """按关键词搜索适配记录（标题或内容）。

        Args:
            keyword: 搜索关键词。
            limit: 返回数量上限。

        Returns:
            记录字典列表。
        """
        conn = self._get_conn()
        pattern = f"%{keyword}%"
        rows = conn.execute(
            """
            SELECT * FROM adapt_records
            WHERE source_title LIKE ? OR adapted_title LIKE ? OR adapted_content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (pattern, pattern, pattern, limit),
        ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_stats(self) -> dict[str, Any]:
        """获取适配统计信息。

        Returns:
            统计信息字典，包含：
            - total: 总适配次数
            - by_platform: 各平台适配次数
            - first_record: 最早记录时间
            - last_record: 最近记录时间
        """
        conn = self._get_conn()
        total = conn.execute("SELECT COUNT(*) FROM adapt_records").fetchone()[0]

        platform_rows = conn.execute(
            """
            SELECT platform, platform_name, COUNT(*) as count
            FROM adapt_records
            GROUP BY platform
            ORDER BY count DESC
            """
        ).fetchall()

        by_platform = {
            row["platform"]: {
                "name": row["platform_name"],
                "count": row["count"],
            }
            for row in platform_rows
        }

        first_row = conn.execute(
            "SELECT MIN(created_at) as first FROM adapt_records"
        ).fetchone()
        last_row = conn.execute(
            "SELECT MAX(created_at) as last FROM adapt_records"
        ).fetchone()

        return {
            "total": total,
            "by_platform": by_platform,
            "first_record": first_row["first"] if first_row else None,
            "last_record": last_row["last"] if last_row else None,
        }

    def delete(self, record_id: int) -> bool:
        """删除一条适配记录。

        Args:
            record_id: 记录 ID。

        Returns:
            是否删除成功。
        """
        conn = self._get_conn()
        cursor = conn.execute(
            "DELETE FROM adapt_records WHERE id = ?", (record_id,)
        )
        conn.commit()
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info(f"已删除适配记录 #{record_id}")
        return deleted

    def clear(self, before_date: Optional[str] = None) -> int:
        """清除历史记录。

        Args:
            before_date: 清除此日期之前的记录 (YYYY-MM-DD)。
                        若为 None，则清除所有记录。

        Returns:
            删除的记录数。
        """
        conn = self._get_conn()
        if before_date:
            end_dt = f"{before_date}T23:59:59"
            cursor = conn.execute(
                "DELETE FROM adapt_records WHERE adapted_at < ?", (end_dt,)
            )
        else:
            cursor = conn.execute("DELETE FROM adapt_records")
        conn.commit()
        count = cursor.rowcount
        logger.info(f"已清除 {count} 条适配记录")
        return count

    def export_json(self, output_path: str, platform: Optional[str] = None) -> Path:
        """导出历史记录为 JSON 文件。

        Args:
            output_path: 输出文件路径。
            platform: 按平台筛选（可选）。

        Returns:
            输出文件路径。
        """
        records = self.list_recent(limit=10000, platform=platform)
        path = Path(output_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info(f"已导出 {len(records)} 条记录到 {path}")
        return path

    def close(self) -> None:
        """关闭数据库连接。"""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        """将数据库行转换为字典，反序列化 JSON 字段。"""
        d = dict(row)
        for field in ("tags", "title_candidates", "metadata"):
            if field in d and isinstance(d[field], str):
                try:
                    d[field] = json.loads(d[field])
                except json.JSONDecodeError:
                    d[field] = []
        return d
