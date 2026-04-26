"""Publisher (Exporter) 模块测试。"""
from __future__ import annotations

import tempfile
import pytest
from pathlib import Path

from ai_content_multiplatform.core.publisher import ContentExporter
from ai_content_multiplatform.core.models import AdaptedContent

def test_export_xiaohongshu():
    exporter = ContentExporter()
    adapted = AdaptedContent(
        platform="xiaohongshu", platform_name="小红书",
        title="Test Post", content="Some content", tags=["a", "b"]
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = exporter.export(adapted, Path(tmpdir))
        assert out_path.exists()
        text = out_path.read_text()
        assert "【标题】" in text
        assert "#a" in text

def test_export_weixin():
    exporter = ContentExporter()
    adapted = AdaptedContent(
        platform="weixin", platform_name="微信",
        title="WeChat Post", content="Content", tags=[]
    )
    
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = exporter.export(adapted, Path(tmpdir))
        assert out_path.exists()
        text = out_path.read_text()
        assert text.startswith("# ")

def test_export_batch():
    exporter = ContentExporter()
    contents = [
        AdaptedContent(platform="p1", platform_name="P1", title="T1", content="C1", tags=[]),
        AdaptedContent(platform="p2", platform_name="P2", title="T2", content="C2", tags=[]),
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = exporter.export_batch(contents, Path(tmpdir))
        assert len(paths) == 2
        assert all(p.exists() for p in paths)
