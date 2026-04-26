"""日志工具。"""

from __future__ import annotations

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

_console = Console(stderr=True)


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """获取配置好的 Logger 实例。"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())
    handler = RichHandler(
        console=_console,
        show_path=False,
        rich_tracebacks=True,
    )
    formatter = logging.Formatter(
        "%(message)s",
        datefmt="[%X]",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
