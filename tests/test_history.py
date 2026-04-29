"""适配历史记录模块测试。"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from ai_content_multiplatform.core.history import AdaptHistory
from ai_content_multiplatform.core.models import AdaptedContent


@pytest.fixture
def history(tmp_path: Path) -> AdaptHistory:
    """创建临时数据库的历史记录管理器。"""
    db_path = str(tmp_path / "test_history.db")
    return AdaptHistory(db_path=db_path)


@pytest.fixture
def sample_adapted() -> AdaptedContent:
    """创建示例适配内容。"""
    return AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="微信适配标题",
        content="这是微信适配后的内容",
        tags=["AI", "技术"],
        title_candidates=["候选标题1", "候选标题2"],
        cover_suggestion="科技感封面",
        adapted_at=datetime.now(),
    )


@pytest.fixture
def sample_adapted_zhihu() -> AdaptedContent:
    """创建知乎适配内容。"""
    return AdaptedContent(
        platform="zhihu",
        platform_name="知乎",
        title="知乎适配标题",
        content="这是知乎适配后的内容，更加深入",
        tags=["人工智能", "深度学习", "LLM"],
        adapted_at=datetime.now(),
    )


class TestAdaptHistorySave:
    """测试保存功能。"""

    def test_save_single_record(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """保存单条记录。"""
        record_id = history.save(sample_adapted, source_title="原始标题")
        assert record_id > 0

    def test_save_with_metadata(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """保存带元数据的记录。"""
        metadata = {"llm_model": "gpt-4o-mini", "elapsed": 3.5}
        record_id = history.save(sample_adapted, metadata=metadata)
        records = history.list_recent(limit=1)
        assert records[0]["metadata"]["llm_model"] == "gpt-4o-mini"
        assert records[0]["metadata"]["elapsed"] == 3.5

    def test_save_batch(self, history: AdaptHistory, sample_adapted: AdaptedContent, sample_adapted_zhihu: AdaptedContent) -> None:
        """批量保存记录。"""
        ids = history.save_batch([sample_adapted, sample_adapted_zhihu], source_title="原始标题")
        assert len(ids) == 2
        assert all(i > 0 for i in ids)


class TestAdaptHistoryQuery:
    """测试查询功能。"""

    def test_list_recent_empty(self, history: AdaptHistory) -> None:
        """空数据库查询。"""
        records = history.list_recent()
        assert records == []

    def test_list_recent_with_data(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """有数据时查询。"""
        history.save(sample_adapted)
        records = history.list_recent()
        assert len(records) == 1
        assert records[0]["platform"] == "weixin"
        assert records[0]["adapted_title"] == "微信适配标题"

    def test_list_recent_by_platform(self, history: AdaptHistory, sample_adapted: AdaptedContent, sample_adapted_zhihu: AdaptedContent) -> None:
        """按平台筛选。"""
        history.save(sample_adapted)
        history.save(sample_adapted_zhihu)

        weixin_records = history.list_recent(platform="weixin")
        assert len(weixin_records) == 1
        assert weixin_records[0]["platform"] == "weixin"

        zhihu_records = history.list_recent(platform="zhihu")
        assert len(zhihu_records) == 1
        assert zhihu_records[0]["platform"] == "zhihu"

    def test_list_recent_limit(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """限制返回数量。"""
        for i in range(5):
            adapted = AdaptedContent(
                platform="weixin",
                platform_name="微信公众号",
                title=f"标题{i}",
                content=f"内容{i}",
                adapted_at=datetime.now(),
            )
            history.save(adapted)

        records = history.list_recent(limit=3)
        assert len(records) == 3

    def test_search_by_keyword(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """关键词搜索。"""
        history.save(sample_adapted, source_title="深度学习入门指南")
        results = history.search("深度学习")
        assert len(results) == 1

    def test_search_by_title(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """按适配标题搜索。"""
        history.save(sample_adapted)
        results = history.search("微信适配")
        assert len(results) == 1

    def test_search_no_match(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """搜索无匹配。"""
        history.save(sample_adapted)
        results = history.search("不存在的关键词")
        assert len(results) == 0


class TestAdaptHistoryStats:
    """测试统计功能。"""

    def test_stats_empty(self, history: AdaptHistory) -> None:
        """空数据库统计。"""
        stats = history.get_stats()
        assert stats["total"] == 0
        assert stats["by_platform"] == {}

    def test_stats_with_data(self, history: AdaptHistory, sample_adapted: AdaptedContent, sample_adapted_zhihu: AdaptedContent) -> None:
        """有数据时统计。"""
        history.save(sample_adapted)
        history.save(sample_adapted_zhihu)
        history.save(sample_adapted)

        stats = history.get_stats()
        assert stats["total"] == 3
        assert stats["by_platform"]["weixin"]["count"] == 2
        assert stats["by_platform"]["zhihu"]["count"] == 1


class TestAdaptHistoryDelete:
    """测试删除功能。"""

    def test_delete_record(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """删除记录。"""
        record_id = history.save(sample_adapted)
        assert history.delete(record_id) is True
        records = history.list_recent()
        assert len(records) == 0

    def test_delete_nonexistent(self, history: AdaptHistory) -> None:
        """删除不存在的记录。"""
        assert history.delete(9999) is False

    def test_clear_all(self, history: AdaptHistory, sample_adapted: AdaptedContent) -> None:
        """清除所有记录。"""
        history.save(sample_adapted)
        count = history.clear()
        assert count == 1
        records = history.list_recent()
        assert len(records) == 0


class TestAdaptHistoryExport:
    """测试导出功能。"""

    def test_export_json(self, history: AdaptHistory, sample_adapted: AdaptedContent, tmp_path: Path) -> None:
        """导出为 JSON。"""
        history.save(sample_adapted)
        output = str(tmp_path / "export.json")
        result_path = history.export_json(output)
        assert result_path.exists()

        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["platform"] == "weixin"

    def test_export_json_by_platform(
        self, history: AdaptHistory, sample_adapted: AdaptedContent,
        sample_adapted_zhihu: AdaptedContent, tmp_path: Path,
    ) -> None:
        """按平台导出。"""
        history.save(sample_adapted)
        history.save(sample_adapted_zhihu)

        output = str(tmp_path / "weixin_export.json")
        result_path = history.export_json(output, platform="weixin")

        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["platform"] == "weixin"
