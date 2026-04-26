"""自定义异常类。"""

from __future__ import annotations


class ContentParserError(Exception):
    """内容解析异常。"""
    pass


class LLMCallError(Exception):
    """LLM 调用异常。"""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AdapterError(Exception):
    """内容适配异常。"""
    pass


class ValidationError(Exception):
    """内容验证异常。"""
    def __init__(self, message: str, detail: str | None = None):
        super().__init__(message)
        self.detail = detail


class PublishError(Exception):
    """发布异常。"""
    def __init__(self, message: str, platform: str | None = None):
        super().__init__(message)
        self.platform = platform


class ConfigError(Exception):
    """配置异常。"""
    pass
