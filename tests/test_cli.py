"""CLI 命令测试。"""
from __future__ import annotations

import pytest
from typer.testing import CliRunner

from ai_content_multiplatform.cli.main import app

runner = CliRunner()


def test_cli_help() -> None:
    """测试 CLI 帮助信息。"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "adapt" in result.output
    assert "preview" in result.output
    assert "publish" in result.output


def test_cli_adapt_file_not_found() -> None:
    """测试 adapt 命令文件不存在。"""
    result = runner.invoke(app, ["adapt", "nonexistent.md"])
    assert result.exit_code == 1


def test_cli_preview_file_not_found() -> None:
    """测试 preview 命令文件不存在。"""
    result = runner.invoke(app, ["preview", "nonexistent.md", "weixin"])
    assert result.exit_code == 1


def test_cli_config_show() -> None:
    """测试 config show 命令。"""
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0


def test_cli_config_rules() -> None:
    """测试 config rules 命令。"""
    result = runner.invoke(app, ["config", "rules"])
    assert result.exit_code == 0


def test_cli_publish_file_not_found() -> None:
    """测试 publish 命令文件不存在。"""
    result = runner.invoke(app, ["publish", "nonexistent.md"])
    assert result.exit_code == 1
