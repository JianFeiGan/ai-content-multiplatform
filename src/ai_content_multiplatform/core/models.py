"""核心数据结构定义。"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ContentInput(BaseModel):
    """用户输入的原始内容。"""
    title: str = Field(..., description="文章标题")
    content: str = Field(..., description="正文内容（Markdown 格式）")
    tags: list[str] = Field(default_factory=list, description="标签列表")
    images: list[str] = Field(default_factory=list, description="图片 URL 列表")
    author: Optional[str] = Field(default=None, description="作者")


class PlatformRule(BaseModel):
    """单个平台的适配规则。"""
    name: str = Field(..., description="平台中文名")
    title_max_len: int = Field(..., description="标题最大长度")
    content_max_len: int = Field(..., description="内容最大长度")
    tag_limit: int = Field(..., description="标签数量限制")
    cover_size: tuple[int, int] = Field(..., description="封面图尺寸 (宽, 高)")
    style_prompt: str = Field(..., description="LLM 风格提示词")
    forbidden_words: list[str] = Field(default_factory=list, description="禁用词列表")
    notes: str = Field(default="", description="平台特殊说明")


class AdaptedContent(BaseModel):
    """适配后的单平台内容。"""
    platform: str = Field(..., description="平台标识（如 weixin, zhihu）")
    platform_name: str = Field(..., description="平台中文名")
    title: str = Field(..., description="适配后的标题")
    title_candidates: list[str] = Field(default_factory=list, description="备选标题列表")
    content: str = Field(..., description="适配后的正文")
    tags: list[str] = Field(default_factory=list, description="推荐标签")
    cover_suggestion: Optional[str] = Field(default=None, description="封面图建议描述")
    adapted_at: datetime = Field(default_factory=datetime.now, description="适配时间")


class PlatformResult(BaseModel):
    """多平台适配结果汇总。"""
    source_title: str
    source_content: str
    platforms: list[AdaptedContent]
    adapted_at: datetime = Field(default_factory=datetime.now)
