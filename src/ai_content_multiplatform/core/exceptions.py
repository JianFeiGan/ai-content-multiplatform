"""自定义异常类。"""

from __future__ import annotations


class BaseError(Exception):
    """基础异常类，所有自定义异常的基类。"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ParseError(BaseError):
    """内容解析异常。"""
    pass


class LLMError(BaseError):
    """LLM 调用异常。"""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AdapterError(BaseError):
    """内容适配异常。"""
    pass


class ValidationError(BaseError):
    """内容验证异常。"""

    def __init__(self, message: str, detail: str | None = None):
        super().__init__(message)
        self.detail = detail


class PublishError(BaseError):
    """发布异常。"""

    def __init__(self, message: str, platform: str | None = None):
        super().__init__(message)
        self.platform = platform


class ConfigError(BaseError):
    """配置异常。"""
    pass


class PlatformError(BaseError):
    """平台操作异常。"""
    pass


# 别名兼容
ContentParserError = ParseError
LLMCallError = LLMError
