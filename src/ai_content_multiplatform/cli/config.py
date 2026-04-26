"""Config command - manage application settings."""
from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_content_multiplatform.config.settings import AppConfig

console = Console()
config_cmd = typer.Typer()


@config_cmd.command("show")
def show() -> None:
    """显示当前配置。"""
    settings = AppConfig()
    console.print("[bold]⚙ 当前配置[/]")

    table = Table()
    table.add_column("配置项", style="cyan")
    table.add_column("值", style="green")

    table.add_row("默认模型", settings.default_model)
    table.add_row("默认温度", str(settings.default_temperature))
    table.add_row("API Key", "****" if settings.openai_api_key else "未设置")
    table.add_row("Base URL", settings.openai_base_url or "默认")

    console.print(table)


@config_cmd.command("rules")
def rules() -> None:
    """显示平台规则摘要。"""
    settings = AppConfig()
    all_rules = settings.get_platform_rules()

    table = Table(title="📋 平台规则")
    table.add_column("平台", style="cyan")
    table.add_column("标题限制", style="yellow")
    table.add_column("内容限制", style="yellow")
    table.add_column("标签限制", style="magenta")

    for pid, rule in all_rules.items():
        table.add_row(
            rule.name,
            f"≤{rule.title_max_len}",
            f"≤{rule.content_max_len}",
            f"≤{rule.tag_limit}",
        )

    console.print(table)


@config_cmd.command("history")
def history() -> None:
    """查看发布历史。"""
    from ai_content_multiplatform.core.publisher import Publisher

    publisher = Publisher()
    records = publisher.get_history()

    if not records:
        console.print("📭 暂无发布记录")
        return

    table = Table(title="📜 发布历史")
    table.add_column("时间", style="cyan")
    table.add_column("平台", style="green")
    table.add_column("标题", style="yellow")
    table.add_column("状态", style="magenta")

    for record in records[-20:]:  # 最近 20 条
        table.add_row(
            record.get("published_at", "N/A")[:19],
            record.get("platform", "N/A"),
            record.get("title", "N/A")[:30],
            record.get("status", "N/A"),
        )

    console.print(table)
