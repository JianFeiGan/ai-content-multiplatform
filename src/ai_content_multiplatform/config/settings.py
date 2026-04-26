"""全局配置管理。"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_content_multiplatform.core.models import PlatformRule


class Defaults(BaseModel):
    """LLM 默认配置。"""
    llm_model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 4000
    title_candidates: int = 3


class LLMConfig(BaseModel):
    """LLM 配置。"""
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 4000


class PlatformRulesConfig(BaseModel):
    """平台规则配置文件结构。"""
    platforms: dict[str, dict]
    defaults: Defaults = Field(default_factory=Defaults)


class AppConfig(BaseSettings):
    """应用程序全局配置。"""

    model_config = SettingsConfigDict(
        env_prefix="AI_CONTENT_",
        env_file=".env",
        extra="ignore",
    )

    openai_api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API Key",
    )
    openai_base_url: Optional[str] = Field(
        default=None,
        description="OpenAI API Base URL",
    )
    default_model: str = "gpt-4o-mini"
    default_temperature: float = 0.7

    @property
    def llm(self) -> LLMConfig:
        """获取 LLM 配置。"""
        return LLMConfig(
            model=self.default_model,
            temperature=self.default_temperature,
        )

    @property
    def default_platforms(self) -> list[str]:
        """获取默认平台列表。"""
        return ["weixin", "zhihu", "douyin", "xiaohongshu", "csdn", "juejin", "toutiao"]

    @property
    def output_dir(self) -> Path:
        """获取输出目录。"""
        return Path("./output")

    @staticmethod
    def load_rules(rules_path: Optional[str] = None) -> PlatformRulesConfig:
        """加载平台规则配置文件。"""
        if rules_path is None:
            rules_path = str(Path(__file__).parent / "rules.yaml")

        with open(rules_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        return PlatformRulesConfig(**raw)

    def get_platform_rules(self) -> dict[str, PlatformRule]:
        """获取所有平台规则，返回字典 {platform_id: PlatformRule}。"""
        config = self.load_rules()
        rules: dict[str, PlatformRule] = {}
        for platform_id, data in config.platforms.items():
            rules[platform_id] = PlatformRule(**data)
        return rules

    def get_platform_rule(self, platform_id: str) -> Optional[PlatformRule]:
        """获取单个平台规则。"""
        rules = self.get_platform_rules()
        return rules.get(platform_id)


# 别名，供 CLI 使用
Settings = AppConfig
