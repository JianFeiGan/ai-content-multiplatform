"""Adapt command - adapt content to multiple platforms."""
from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ai_content_multiplatform.config.settings import AppConfig
from ai_content_multiplatform.core.parser import parse_file
from ai_content_multiplatform.core.adapter import ContentAdapter

console = Console()


def adapt_cmd(
    input_file: str = typer.Argument(..., help="输入内容文件 (Markdown)"),
    platforms: str = typer.Option("all", "--platforms", "-p", help="目标平台，逗号分隔或 all"),
    output_dir: str = typer.Option(None, "--output", "-o", help="输出目录"),
    dry_run: bool = typer.Option(False, "--dry-run", help="仅显示适配计划，不执行"),
) -> None:
    """从 Markdown 文件适配内容到多平台。"""
    input_path = Path(input_file).expanduser()
    if not input_path.exists():
        console.print(f"[red]✗[/] 文件不存在：{input_path}")
        raise typer.Exit(1)

    console.print(f"[bold]📖 读取内容：[/]{input_path}")

    settings = AppConfig()
    content = parse_file(str(input_path))

    console.print(f"[bold]📝 解析完成：[/]{content.title} ({len(content.content)} 字符)")

    # 确定目标平台
    all_rules = settings.get_platform_rules()
    if platforms == "all":
        target_platforms = list(all_rules.keys())
    else:
        target_platforms = [p.strip() for p in platforms.split(",")]

    console.print(f"[bold]🎯 目标平台：[/]{', '.join(target_platforms)}")

    if dry_run:
        console.print("[yellow]⚠ Dry run mode - 显示适配计划[/]")
        for platform in target_platforms:
            rule = all_rules.get(platform)
            if rule:
                console.print(f"  • {platform}: 标题≤{rule.title_max_len}, 标签≤{rule.tag_limit}")
        return

    # 适配内容
    console.print("[bold]🔄 开始适配...[/]")
    adapter = ContentAdapter(settings=settings)

    results = {}
    for platform in target_platforms:
        console.print(f"  → 适配 {platform}...", end="")
        try:
            adapted = adapter.adapt(content, platform)
            results[platform] = adapted
            console.print(" [green]✓[/]")
        except Exception as e:
            console.print(f" [red]✗ {e}[/]")

    # 保存结果
    out_dir = Path(output_dir).expanduser() if output_dir else Path("./adapted")
    out_dir.mkdir(parents=True, exist_ok=True)

    for platform, adapted in results.items():
        safe_title = adapted.title[:30].replace("/", "_").replace("\\", "_")
        output_file = out_dir / f"{platform}_{safe_title}.md"
        output_file.write_text(
            f"# {adapted.title}\n\n{adapted.content}\n\n"
            f"Tags: {', '.join(adapted.tags)}\n",
            encoding="utf-8",
        )
        console.print(f"  💾 已保存：{output_file}")

    # 汇总表
    table = Table(title="✅ 适配完成")
    table.add_column("平台", style="cyan")
    table.add_column("标题", style="green")
    table.add_column("内容长度", style="yellow")
    table.add_column("标签数", style="magenta")

    for platform, adapted in results.items():
        table.add_row(
            platform,
            adapted.title[:40],
            f"{len(adapted.content)} 字符",
            str(len(adapted.tags)),
        )

    console.print(table)
