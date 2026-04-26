"""Adapt command - adapt content to different platforms."""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

import typer
from rich.console import Console

from ai_content_multiplatform.config.settings import AppConfig
from ai_content_multiplatform.core.parser import parse_file
from ai_content_multiplatform.core.adapter import ContentAdapter
from ai_content_multiplatform.core.llm import LLMClient
from ai_content_multiplatform.utils.formatter import format_adapted_content

console = Console()

def adapt_cmd(
    input_file: str = typer.Argument(..., help="输入内容文件 (Markdown)"),
    platforms: str = typer.Option("all", "--platforms", "-p", help="目标平台，逗号分隔"),
    output_dir: str = typer.Option("./output", "--output", "-o", help="输出目录"),
    use_llm: bool = typer.Option(True, "--llm/--no-llm", help="是否使用 LLM 进行智能适配"),
    dry_run: bool = typer.Option(False, "--dry-run", help="仅显示计划，不调用 API"),
) -> None:
    """适配内容到指定平台。"""
    input_path = Path(input_file).expanduser()
    if not input_path.exists():
        console.print(f"[red]✗[/] 文件不存在：{input_path}")
        raise typer.Exit(1)

    settings = AppConfig()
    content = parse_file(str(input_path))
    console.print(f"[bold]📖 读取内容：[/]{content.title} ({len(content.content)} 字符)")

    # LLM 初始化
    llm_client = None
    if use_llm and not dry_run:
        api_key = os.getenv("OPENAI_API_KEY") or settings.openai_api_key
        if api_key:
            llm_client = LLMClient(
                api_key=api_key,
                base_url=os.getenv("OPENAI_BASE_URL") or settings.openai_base_url,
                model=settings.default_model,
            )
            console.print(f"[bold green]🤖 LLM 已启用:[/] {settings.default_model}")
        else:
            console.print("[yellow]⚠ 未检测到 OPENAI_API_KEY，降级为规则适配[/]")
    
    adapter = ContentAdapter(settings=settings, llm_client=llm_client)

    all_rules = settings.get_platform_rules()
    if platforms == "all":
        target_platforms = list(all_rules.keys())
    else:
        target_platforms = [p.strip() for p in platforms.split(",")]

    console.print(f"[bold]🎯 目标平台：[/]{', '.join(target_platforms)}")
    console.print("[bold]🔄 开始适配...[/]")

    if dry_run:
        for p in target_platforms:
            console.print(f"  → 将适配 {p}")
        return

    async def run_adapt():
        results = []
        for pid in target_platforms:
            try:
                if llm_client:
                    adapted = await adapter.adapt_with_llm_async(content, pid)
                else:
                    adapted = adapter.adapt(content, pid)
                results.append(adapted)
                console.print(f"  ✓ {pid} 适配完成")
            except Exception as e:
                console.print(f"  ✗ {pid} 适配失败：{e}")
        return results

    adapted_list = asyncio.run(run_adapt())

    # 保存结果
    out_path = Path(output_dir).expanduser()
    out_path.mkdir(parents=True, exist_ok=True)
    
    for adapted in adapted_list:
        formatted = format_adapted_content(adapted)
        file_name = f"{adapted.platform}_{adapted.title[:20]}.md"
        file_path = out_path / file_name
        formatted.save(file_path)
        console.print(f"  💾 已保存：{file_path}")

    console.print(f"[bold green]✨ 适配完成！文件已保存至 {out_path}[/]")

