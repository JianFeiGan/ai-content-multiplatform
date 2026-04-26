"""Publish command - 导出适配内容到文件。"""
from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_content_multiplatform.config.settings import AppConfig
from ai_content_multiplatform.core.parser import parse_file
from ai_content_multiplatform.core.adapter import ContentAdapter
from ai_content_multiplatform.core.publisher import ContentExporter

console = Console()

def publish_cmd(
    input_file: str = typer.Argument(..., help="输入内容文件 (Markdown)"),
    platforms: str = typer.Option("all", "--platforms", "-p", help="目标平台，逗号分隔"),
    output_dir: str = typer.Option("./output", "--output", "-o", help="导出目录"),
    use_llm: bool = typer.Option(False, "--llm", help="发布前重新使用 LLM 适配"),
) -> None:
    """读取内容文件并导出为各平台专用格式。"""
    input_path = Path(input_file).expanduser()
    if not input_path.exists():
        console.print(f"[red]✗[/] 文件不存在：{input_path}")
        raise typer.Exit(1)

    settings = AppConfig()
    content = parse_file(str(input_path))
    
    # 初始化适配器
    llm_client = None
    if use_llm:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            from ai_content_multiplatform.core.llm import LLMClient
            llm_client = LLMClient(api_key=api_key, base_url=settings.openai_base_url)
            console.print("[bold green]🤖 LLM 模式已启用[/]")

    adapter = ContentAdapter(settings=settings, llm_client=llm_client)
    exporter = ContentExporter()

    all_rules = settings.get_platform_rules()
    if platforms == "all":
        target_platforms = list(all_rules.keys())
    else:
        target_platforms = [p.strip() for p in platforms.split(",")]

    out_path = Path(output_dir).expanduser()
    console.print(f"[bold]📤 正在导出到 {out_path} ...[/]")

    import asyncio

    async def run_export():
        results = []
        for pid in target_platforms:
            try:
                if llm_client:
                    adapted = await adapter.adapt_with_llm_async(content, pid)
                else:
                    # 尝试读取已有的输出文件，或者直接适配
                    # 这里简化为重新适配
                    adapted = adapter.adapt(content, pid)
                
                file_path = exporter.export(adapted, out_path)
                results.append((adapted.platform, "成功", str(file_path)))
                console.print(f"  ✓ {pid} -> {file_path.name}")
            except Exception as e:
                results.append((pid, f"失败: {e}", "N/A"))
                console.print(f"  ✗ {pid} 失败：{e}")
        return results

    results = asyncio.run(run_export())

    # 汇总表
    table = Table(title="📊 导出结果")
    table.add_column("平台", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("路径", style="yellow")

    for platform, status, path in results:
        table.add_row(platform, status, path)

    console.print(table)
