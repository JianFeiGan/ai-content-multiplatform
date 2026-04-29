"""CLI 命令测试 - 覆盖所有子命令和边界场景。"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_content_multiplatform.cli.main import app

runner = CliRunner()


# ─── 帮助和版本 ───


def test_cli_help() -> None:
    """测试 CLI 帮助信息。"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "adapt" in result.output
    assert "preview" in result.output
    assert "publish" in result.output
    assert "config" in result.output


def test_cli_adapt_help() -> None:
    """测试 adapt 命令帮助。"""
    result = runner.invoke(app, ["adapt", "--help"])
    assert result.exit_code == 0
    assert "输入内容文件" in result.output or "INPUT_FILE" in result.output


def test_cli_preview_help() -> None:
    """测试 preview 命令帮助。"""
    result = runner.invoke(app, ["preview", "--help"])
    assert result.exit_code == 0


def test_cli_publish_help() -> None:
    """测试 publish 命令帮助。"""
    result = runner.invoke(app, ["publish", "--help"])
    assert result.exit_code == 0


def test_cli_config_help() -> None:
    """测试 config 命令帮助。"""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0


# ─── adapt 命令 ───


def test_cli_adapt_file_not_found() -> None:
    """测试 adapt 命令文件不存在。"""
    result = runner.invoke(app, ["adapt", "nonexistent.md"])
    assert result.exit_code == 1


def test_cli_adapt_with_valid_file() -> None:
    """测试 adapt 命令使用有效文件（规则模式，不使用 LLM）。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("---\ntitle: 测试文章\ntags: [AI, 技术]\nauthor: 测试\n---\n\n# 测试文章\n\n这是一篇测试文章的内容。")
        f.flush()
        temp_path = f.name

    try:
        result = runner.invoke(app, [
            "adapt", temp_path,
            "--no-llm",
            "--platforms", "weixin,zhihu",
        ])
        # 不使用 LLM 的规则适配应该成功
        assert result.exit_code == 0
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_cli_adapt_dry_run() -> None:
    """测试 adapt 命令 dry-run 模式。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# 测试文章\n\n这是测试内容")
        f.flush()
        temp_path = f.name

    try:
        result = runner.invoke(app, [
            "adapt", temp_path,
            "--dry-run",
        ])
        assert result.exit_code == 0
    finally:
        Path(temp_path).unlink(missing_ok=True)


def test_cli_adapt_all_platforms() -> None:
    """测试 adapt 命令适配所有平台。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# 测试文章\n\n这是测试内容")
        f.flush()
        temp_path = f.name

    try:
        result = runner.invoke(app, [
            "adapt", temp_path,
            "--no-llm",
            "--platforms", "all",
        ])
        assert result.exit_code == 0
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ─── preview 命令 ───


def test_cli_preview_file_not_found() -> None:
    """测试 preview 命令文件不存在。"""
    result = runner.invoke(app, ["preview", "nonexistent.md", "weixin"])
    assert result.exit_code == 1


def test_cli_preview_valid_file() -> None:
    """测试 preview 命令使用有效文件。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# 测试文章\n\n这是测试内容")
        f.flush()
        temp_path = f.name

    try:
        result = runner.invoke(app, ["preview", temp_path, "weixin"])
        assert result.exit_code == 0
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ─── publish 命令 ───


def test_cli_publish_file_not_found() -> None:
    """测试 publish 命令文件不存在。"""
    result = runner.invoke(app, ["publish", "nonexistent.md"])
    assert result.exit_code == 1


def test_cli_publish_valid_file() -> None:
    """测试 publish 命令使用有效文件。"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write("# 测试文章\n\n这是测试内容")
        f.flush()
        temp_path = f.name

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # publish 默认不使用 LLM，不需要 --no-llm 标志
            result = runner.invoke(app, [
                "publish", temp_path,
                "--platforms", "weixin",
                "--output", tmpdir,
            ])
            assert result.exit_code == 0
        finally:
            Path(temp_path).unlink(missing_ok=True)


# ─── config 命令 ───


def test_cli_config_show() -> None:
    """测试 config show 命令。"""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0


def test_cli_config_rules() -> None:
    """测试 config rules 命令。"""
    result = runner.invoke(app, ["config", "rules"])
    assert result.exit_code == 0
    assert "平台规则" in result.output


def test_cli_config_history() -> None:
    """测试 config history 命令。"""
    result = runner.invoke(app, ["config", "history"])
    assert result.exit_code == 0


def test_cli_config_stats() -> None:
    """测试 config stats 命令。"""
    result = runner.invoke(app, ["config", "stats"])
    assert result.exit_code == 0


def test_cli_config_search() -> None:
    """测试 config search 命令。"""
    result = runner.invoke(app, ["config", "search", "测试"])
    assert result.exit_code == 0
