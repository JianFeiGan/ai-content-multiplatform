"""Config command - manage application settings and history."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ai_content_multiplatform.config.settings import AppConfig

console = Console()
config_cmd = typer.Typer(help="配置与历史管理")


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
def history(
    limit: int = typer.Option(20, "--limit", "-n", help="显示条数"),
    platform: str = typer.Option(None, "--platform", "-p", help="按平台筛选"),
) -> None:
    """查看适配历史记录。"""
    from ai_content_multiplatform.core.history import AdaptHistory

    hist = AdaptHistory()
    records = hist.list_recent(limit=limit, platform=platform)

    if not records:
        console.print("[dim]暂无适配记录[/]")
        return

    table = Table(title=f"📜 适配历史（最近 {len(records)} 条）")
    table.add_column("#", style="dim", width=5)
    table.add_column("时间", style="cyan", width=20)
    table.add_column("平台", style="green", width=10)
    table.add_column("适配标题", style="white", max_width=40)
    table.add_column("标签", style="magenta", max_width=20)

    for rec in records:
        tags_str = ", ".join(rec.get("tags", [])[:3])
        if len(rec.get("tags", [])) > 3:
            tags_str += "..."
        table.add_row(
            str(rec["id"]),
            rec.get("created_at", "")[:19],
            rec.get("platform_name", ""),
            rec.get("adapted_title", "")[:40],
            tags_str,
        )

    console.print(table)
    hist.close()


@config_cmd.command("stats")
def stats() -> None:
    """查看适配统计信息。"""
    from ai_content_multiplatform.core.history import AdaptHistory

    hist = AdaptHistory()
    data = hist.get_stats()

    console.print(Panel(
        f"[bold]总适配次数：[/]{data['total']}\n"
        f"[bold]首次记录：[/]{data.get('first_record', '无')}\n"
        f"[bold]最近记录：[/]{data.get('last_record', '无')}",
        title="📊 适配统计",
        border_style="blue",
    ))

    if data["by_platform"]:
        table = Table(title="各平台适配次数")
        table.add_column("平台", style="cyan")
        table.add_column("次数", style="green", justify="right")

        for pid, info in data["by_platform"].items():
            table.add_row(info["name"], str(info["count"]))

        console.print(table)

    hist.close()


@config_cmd.command("search")
def search_history(
    keyword: str = typer.Argument(..., help="搜索关键词"),
    limit: int = typer.Option(10, "--limit", "-n", help="显示条数"),
) -> None:
    """搜索适配历史记录。"""
    from ai_content_multiplatform.core.history import AdaptHistory

    hist = AdaptHistory()
    records = hist.search(keyword=keyword, limit=limit)

    if not records:
        console.print(f"[dim]未找到包含「{keyword}」的记录[/]")
        return

    table = Table(title=f"🔍 搜索结果：{keyword}")
    table.add_column("#", style="dim", width=5)
    table.add_column("时间", style="cyan", width=20)
    table.add_column("平台", style="green", width=10)
    table.add_column("适配标题", style="white", max_width=40)

    for rec in records:
        table.add_row(
            str(rec["id"]),
            rec.get("created_at", "")[:19],
            rec.get("platform_name", ""),
            rec.get("adapted_title", "")[:40],
        )

    console.print(table)
    hist.close()
