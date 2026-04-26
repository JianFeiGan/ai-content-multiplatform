"""Preview command - preview adapted content."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from ai_content_multiplatform.config.settings import AppConfig
from ai_content_multiplatform.core.parser import parse_file
from ai_content_multiplatform.core.adapter import ContentAdapter

console = Console()


def preview_cmd(
    input_file: str = typer.Argument(..., help="输入内容文件 (Markdown)"),
    platform: str = typer.Argument(..., help="目标平台（如 weixin, zhihu）"),
) -> None:
    """预览单个平台的适配效果。"""
    input_path = Path(input_file).expanduser()
    if not input_path.exists():
        console.print(f"[red]✗[/] 文件不存在：{input_path}")
        raise typer.Exit(1)

    settings = AppConfig()
    content = parse_file(str(input_path))
    adapter = ContentAdapter(settings=settings)

    console.print(f"[bold]🔍 预览 {platform} 适配效果[/]")

    adapted = adapter.adapt(content, platform)

    console.print(Panel(
        f"[bold]标题：[/]{adapted.title}\n\n"
        f"[bold]内容：[/]\n{adapted.content[:500]}{'...' if len(adapted.content) > 500 else ''}\n\n"
        f"[bold]标签：[/]{', '.join(adapted.tags)}",
        title=f"📱 {adapted.platform_name} 预览",
        border_style="green",
    ))
