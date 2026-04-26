"""Publish command - publish adapted content to platforms."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_content_multiplatform.config.settings import AppConfig
from ai_content_multiplatform.core.parser import parse_file
from ai_content_multiplatform.core.adapter import ContentAdapter
from ai_content_multiplatform.core.publisher import Publisher

console = Console()


def publish_cmd(
    input_file: str = typer.Argument(..., help="输入内容文件 (Markdown)"),
    platforms: str = typer.Option("all", "--platforms", "-p", help="目标平台，逗号分隔"),
    draft: bool = typer.Option(True, "--draft/--publish", help="保存为草稿或直接发布"),
    dry_run: bool = typer.Option(False, "--dry-run", help="模拟发布"),
) -> None:
    """适配并发布内容到指定平台。"""
    input_path = Path(input_file).expanduser()
    if not input_path.exists():
        console.print(f"[red]✗[/] 文件不存在：{input_path}")
        raise typer.Exit(1)

    settings = AppConfig()
    content = parse_file(str(input_path))
    adapter = ContentAdapter(settings=settings)
    publisher = Publisher()

    all_rules = settings.get_platform_rules()
    if platforms == "all":
        target_platforms = list(all_rules.keys())
    else:
        target_platforms = [p.strip() for p in platforms.split(",")]

    console.print(f"[bold]📤 发布到 {len(target_platforms)} 个平台{'[草稿模式]' if draft else ''}[/]")

    if dry_run:
        console.print("[yellow]⚠ Dry run - 模拟发布[/]")
        for platform in target_platforms:
            console.print(f"  → 将发布到 {platform}")
        return

    # 先适配
    adapted_contents = []
    for platform in target_platforms:
        try:
            adapted = adapter.adapt(content, platform)
            adapted_contents.append(adapted)
            console.print(f"  ✓ {platform} 适配完成")
        except Exception as e:
            console.print(f"  ✗ {platform} 适配失败：{e}")

    # 发布
    results = []
    for adapted in adapted_contents:
        try:
            result = publisher.publish(adapted, draft=draft)
            results.append((adapted.platform, "成功", result.get("id", "N/A")))
            console.print(f"  ✓ {adapted.platform} 发布成功")
        except Exception as e:
            results.append((adapted.platform, f"失败: {e}", "N/A"))
            console.print(f"  ✗ {adapted.platform} 发布失败：{e}")

    # 汇总表
    table = Table(title="📊 发布结果")
    table.add_column("平台", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("ID", style="yellow")

    for platform, status, pub_id in results:
        table.add_row(platform, status, pub_id)

    console.print(table)
