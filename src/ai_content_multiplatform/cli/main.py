"""Typer CLI 主入口。"""

from __future__ import annotations

import typer

from ai_content_multiplatform.cli.adapt import adapt_cmd
from ai_content_multiplatform.cli.config import config_cmd
from ai_content_multiplatform.cli.preview import preview_cmd
from ai_content_multiplatform.cli.publish import publish_cmd

app = typer.Typer(
    name="ai-content-multiplatform",
    help="AI 内容多平台适配与发布工具",
    add_completion=False,
    rich_markup_mode="rich",
)

# 注册子命令
app.command("adapt")(adapt_cmd)
app.command("preview")(preview_cmd)
app.command("publish")(publish_cmd)
app.add_typer(config_cmd, name="config")


if __name__ == "__main__":
    app()
