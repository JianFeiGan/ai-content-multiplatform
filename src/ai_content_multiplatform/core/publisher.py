"""内容导出器 - 将适配内容保存为平台专用格式。"""

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime
from typing import Any, Optional, List

from ai_content_multiplatform.core.models import AdaptedContent

class ContentExporter:
    """内容导出器。"""

    def export(
        self,
        adapted: AdaptedContent,
        output_dir: Path,
        fmt: str = "markdown",
    ) -> Path:
        """导出单个平台内容。"""
        output_dir = Path(output_dir).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 安全文件名
        safe_title = "".join(c for c in adapted.title if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title.replace(' ', '_')[:30]
        
        ext = "md" if fmt == "markdown" else "txt"
        filename = f"{adapted.platform}_{safe_title}.{ext}"
        filepath = output_dir / filename
        
        # 根据平台生成不同格式
        if adapted.platform in ["xiaohongshu", "douyin"]:
            content = self._format_social_media(adapted)
        elif adapted.platform == "weixin":
            content = self._format_wechat(adapted)
        else:
            content = f"# {adapted.title}\n\n{adapted.content}\n\nTags: {', '.join(adapted.tags)}"
            
        filepath.write_text(content, encoding="utf-8")
        return filepath

    def _format_social_media(self, adapted: AdaptedContent) -> str:
        """社交媒体格式 (小红书/抖音)：标题 + Emoji 列表 + 标签。"""
        lines = [f"【标题】{adapted.title}", ""]
        lines.append(adapted.content)
        lines.append("")
        lines.append("【标签】")
        lines.append(" ".join([f"#{t}" for t in adapted.tags]))
        return "\n".join(lines)

    def _format_wechat(self, adapted: AdaptedContent) -> str:
        """微信公众号格式：Markdown。"""
        lines = [f"# {adapted.title}", ""]
        lines.append(adapted.content)
        if adapted.tags:
            lines.append("")
            lines.append(f"标签：{', '.join(adapted.tags)}")
        return "\n".join(lines)

    def export_batch(
        self,
        contents: List[AdaptedContent],
        output_dir: Path,
    ) -> List[Path]:
        """批量导出。"""
        return [self.export(c, output_dir) for c in contents]

# 别名兼容
Publisher = ContentExporter
