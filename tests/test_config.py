"""Config 模块测试。"""
from __future__ import annotations

import pytest

from ai_content_multiplatform.config.settings import AppConfig


def test_load_rules() -> None:
    """测试加载 rules.yaml。"""
    settings = AppConfig()
    config = settings.load_rules()

    assert "platforms" in config.model_dump()
    assert len(config.platforms) >= 7


def test_get_platform_rules() -> None:
    """测试获取平台规则字典。"""
    settings = AppConfig()
    rules = settings.get_platform_rules()

    assert len(rules) >= 7
    assert "weixin" in rules
    assert "zhihu" in rules
    assert "csdn" in rules
    assert "douyin" in rules
    assert "xiaohongshu" in rules


def test_platform_rule_validation(weixin_rule) -> None:
    """测试 pydantic 验证。"""
    assert weixin_rule.name == "微信公众号"
    assert weixin_rule.title_max_len == 64


def test_platform_rule_missing_field() -> None:
    """测试缺少必填字段抛出异常。"""
    from ai_content_multiplatform.core.models import PlatformRule
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        PlatformRule(
            name="测试",
        )
