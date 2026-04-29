"""Platforms 模块测试 - 全平台适配器验证。"""

from __future__ import annotations

import pytest

from ai_content_multiplatform.platforms.base import BasePlatformAdapter
from ai_content_multiplatform.platforms import PLATFORM_ADAPTERS, get_adapter
from ai_content_multiplatform.core.models import AdaptedContent
from ai_content_multiplatform.core.exceptions import ValidationError


# ─── 基类测试 ───


def test_base_platform_adapter_abstract() -> None:
    """测试基类是抽象类，不能直接实例化。"""
    with pytest.raises(TypeError):
        BasePlatformAdapter()


def test_all_adapters_registered() -> None:
    """测试所有平台适配器都已注册。"""
    expected = {"weixin", "zhihu", "csdn", "douyin", "xiaohongshu", "juejin", "toutiao"}
    assert set(PLATFORM_ADAPTERS.keys()) == expected


def test_get_adapter_valid() -> None:
    """测试获取有效平台适配器。"""
    adapter = get_adapter("weixin")
    assert adapter.platform_id == "weixin"


def test_get_adapter_invalid() -> None:
    """测试获取无效平台适配器抛出异常。"""
    with pytest.raises(ValueError, match="不支持的平台"):
        get_adapter("nonexistent")


# ─── 微信公众号 ───


def test_weixin_adapter_validation() -> None:
    """测试微信公众号适配器验证通过。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="正常标题",
        content="内容",
        tags=[],
    )
    assert adapter.validate_content(content) is True


def test_weixin_adapter_long_title() -> None:
    """测试微信公众号超长标题。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="A" * 65,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="64"):
        adapter.validate_content(content)


def test_weixin_adapter_strip_markdown() -> None:
    """测试微信公众号自动移除 Markdown 标记。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="标题",
        content="**粗体**和```代码```以及##标题",
        tags=[],
    )
    adapter.validate_content(content)
    # validate_content 会自动调用 strip_markdown 修改 content
    assert "**" not in content.content or "```" not in content.content


def test_weixin_adapter_info() -> None:
    """测试微信公众号适配器信息。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    info = adapter.get_platform_info()
    assert info["platform_id"] == "weixin"
    assert info["platform_name"] == "微信公众号"


@pytest.mark.asyncio
async def test_weixin_publish_mock() -> None:
    """测试微信公众号发布（模拟）。"""
    from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter

    adapter = WeixinPlatformAdapter()
    content = AdaptedContent(
        platform="weixin",
        platform_name="微信公众号",
        title="测试标题",
        content="测试内容",
        tags=[],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── 知乎 ───


def test_zhihu_adapter_validation() -> None:
    """测试知乎适配器验证通过。"""
    from ai_content_multiplatform.platforms.zhihu import ZhihuPlatformAdapter

    adapter = ZhihuPlatformAdapter()
    content = AdaptedContent(
        platform="zhihu",
        platform_name="知乎",
        title="正常标题",
        content="深度分析内容",
        tags=["AI"],
    )
    assert adapter.validate_content(content) is True


def test_zhihu_adapter_long_title() -> None:
    """测试知乎超长标题。"""
    from ai_content_multiplatform.platforms.zhihu import ZhihuPlatformAdapter

    adapter = ZhihuPlatformAdapter()
    content = AdaptedContent(
        platform="zhihu",
        platform_name="知乎",
        title="A" * 101,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="100"):
        adapter.validate_content(content)


def test_zhihu_adapter_too_many_tags() -> None:
    """测试知乎标签数量超限。"""
    from ai_content_multiplatform.platforms.zhihu import ZhihuPlatformAdapter

    adapter = ZhihuPlatformAdapter()
    content = AdaptedContent(
        platform="zhihu",
        platform_name="知乎",
        title="标题",
        content="内容",
        tags=["t1", "t2", "t3", "t4", "t5", "t6"],
    )
    with pytest.raises(ValidationError, match="5"):
        adapter.validate_content(content)


@pytest.mark.asyncio
async def test_zhihu_publish_mock() -> None:
    """测试知乎发布（模拟）。"""
    from ai_content_multiplatform.platforms.zhihu import ZhihuPlatformAdapter

    adapter = ZhihuPlatformAdapter()
    content = AdaptedContent(
        platform="zhihu",
        platform_name="知乎",
        title="知乎文章",
        content="深度内容",
        tags=["技术"],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── CSDN ───


def test_csdn_adapter_validation() -> None:
    """测试 CSDN 适配器验证通过。"""
    from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter

    adapter = CSDNPlatformAdapter()
    content = AdaptedContent(
        platform="csdn",
        platform_name="CSDN",
        title="Python 技术详解",
        content="```python\nprint('hello')\n```",
        tags=["Python", "技术"],
    )
    assert adapter.validate_content(content) is True


def test_csdn_adapter_long_title() -> None:
    """测试 CSDN 超长标题。"""
    from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter

    adapter = CSDNPlatformAdapter()
    content = AdaptedContent(
        platform="csdn",
        platform_name="CSDN",
        title="A" * 101,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="100"):
        adapter.validate_content(content)


def test_csdn_adapter_too_many_tags() -> None:
    """测试 CSDN 标签数量超限。"""
    from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter

    adapter = CSDNPlatformAdapter()
    tags = [f"tag{i}" for i in range(11)]
    content = AdaptedContent(
        platform="csdn",
        platform_name="CSDN",
        title="标题",
        content="内容",
        tags=tags,
    )
    with pytest.raises(ValidationError, match="10"):
        adapter.validate_content(content)


def test_csdn_adapter_unspecified_code_blocks() -> None:
    """测试 CSDN 检测未指定语言的代码块（仅警告，不报错）。"""
    from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter

    adapter = CSDNPlatformAdapter()
    content = AdaptedContent(
        platform="csdn",
        platform_name="CSDN",
        title="标题",
        content="```\ncode without language\n```",
        tags=[],
    )
    # 不应抛出异常，只是 warning
    assert adapter.validate_content(content) is True


@pytest.mark.asyncio
async def test_csdn_publish_mock() -> None:
    """测试 CSDN 发布（模拟）。"""
    from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter

    adapter = CSDNPlatformAdapter()
    content = AdaptedContent(
        platform="csdn",
        platform_name="CSDN",
        title="CSDN文章",
        content="技术内容",
        tags=["Python"],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── 掘金 ───


def test_juejin_adapter_validation() -> None:
    """测试掘金适配器验证通过。"""
    from ai_content_multiplatform.platforms.juejin import JuejinPlatformAdapter

    adapter = JuejinPlatformAdapter()
    content = AdaptedContent(
        platform="juejin",
        platform_name="掘金",
        title="前端最佳实践",
        content="技术内容",
        tags=["前端"],
    )
    assert adapter.validate_content(content) is True


def test_juejin_adapter_long_title() -> None:
    """测试掘金超长标题。"""
    from ai_content_multiplatform.platforms.juejin import JuejinPlatformAdapter

    adapter = JuejinPlatformAdapter()
    content = AdaptedContent(
        platform="juejin",
        platform_name="掘金",
        title="A" * 101,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="100"):
        adapter.validate_content(content)


def test_juejin_adapter_too_many_tags() -> None:
    """测试掘金标签数量超限。"""
    from ai_content_multiplatform.platforms.juejin import JuejinPlatformAdapter

    adapter = JuejinPlatformAdapter()
    content = AdaptedContent(
        platform="juejin",
        platform_name="掘金",
        title="标题",
        content="内容",
        tags=["t1", "t2", "t3", "t4", "t5", "t6"],
    )
    with pytest.raises(ValidationError, match="5"):
        adapter.validate_content(content)


@pytest.mark.asyncio
async def test_juejin_publish_mock() -> None:
    """测试掘金发布（模拟）。"""
    from ai_content_multiplatform.platforms.juejin import JuejinPlatformAdapter

    adapter = JuejinPlatformAdapter()
    content = AdaptedContent(
        platform="juejin",
        platform_name="掘金",
        title="掘金文章",
        content="技术深度内容",
        tags=["JavaScript"],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── 头条号 ───


def test_toutiao_adapter_validation() -> None:
    """测试头条号适配器验证通过。"""
    from ai_content_multiplatform.platforms.toutiao import ToutiaoPlatformAdapter

    adapter = ToutiaoPlatformAdapter()
    content = AdaptedContent(
        platform="toutiao",
        platform_name="头条号",
        title="热点新闻速递",
        content="新闻内容",
        tags=["新闻"],
    )
    assert adapter.validate_content(content) is True


def test_toutiao_adapter_long_title() -> None:
    """测试头条号超长标题。"""
    from ai_content_multiplatform.platforms.toutiao import ToutiaoPlatformAdapter

    adapter = ToutiaoPlatformAdapter()
    content = AdaptedContent(
        platform="toutiao",
        platform_name="头条号",
        title="A" * 31,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="30"):
        adapter.validate_content(content)


def test_toutiao_adapter_too_many_tags() -> None:
    """测试头条号标签数量超限。"""
    from ai_content_multiplatform.platforms.toutiao import ToutiaoPlatformAdapter

    adapter = ToutiaoPlatformAdapter()
    content = AdaptedContent(
        platform="toutiao",
        platform_name="头条号",
        title="标题",
        content="内容",
        tags=["t1", "t2", "t3", "t4", "t5", "t6"],
    )
    with pytest.raises(ValidationError, match="5"):
        adapter.validate_content(content)


@pytest.mark.asyncio
async def test_toutiao_publish_mock() -> None:
    """测试头条号发布（模拟）。"""
    from ai_content_multiplatform.platforms.toutiao import ToutiaoPlatformAdapter

    adapter = ToutiaoPlatformAdapter()
    content = AdaptedContent(
        platform="toutiao",
        platform_name="头条号",
        title="头条文章",
        content="新闻内容",
        tags=["科技"],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── 小红书 ───


def test_xiaohongshu_adapter_validation() -> None:
    """测试小红书适配器验证通过。"""
    from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter

    adapter = XiaohongshuPlatformAdapter()
    content = AdaptedContent(
        platform="xiaohongshu",
        platform_name="小红书",
        title="分享好物",
        content="超推荐！",
        tags=["好物"],
    )
    assert adapter.validate_content(content) is True


def test_xiaohongshu_adapter_long_title() -> None:
    """测试小红书超长标题。"""
    from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter

    adapter = XiaohongshuPlatformAdapter()
    content = AdaptedContent(
        platform="xiaohongshu",
        platform_name="小红书",
        title="A" * 21,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="20"):
        adapter.validate_content(content)


def test_xiaohongshu_adapter_content_too_long() -> None:
    """测试小红书内容超长。"""
    from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter

    adapter = XiaohongshuPlatformAdapter()
    content = AdaptedContent(
        platform="xiaohongshu",
        platform_name="小红书",
        title="标题",
        content="A" * 1001,
        tags=[],
    )
    with pytest.raises(ValidationError, match="1000"):
        adapter.validate_content(content)


def test_xiaohongshu_adapter_too_many_tags() -> None:
    """测试小红书标签数量超限。"""
    from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter

    adapter = XiaohongshuPlatformAdapter()
    tags = [f"tag{i}" for i in range(11)]
    content = AdaptedContent(
        platform="xiaohongshu",
        platform_name="小红书",
        title="标题",
        content="内容",
        tags=tags,
    )
    with pytest.raises(ValidationError, match="10"):
        adapter.validate_content(content)


# ─── 抖音 ───


def test_douyin_adapter_validation() -> None:
    """测试抖音适配器验证通过。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="短视频标题",
        content="口播文案",
        tags=["热门"],
    )
    assert adapter.validate_content(content) is True


def test_douyin_adapter_long_title() -> None:
    """测试抖音超长标题。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="A" * 31,
        content="内容",
        tags=[],
    )
    with pytest.raises(ValidationError, match="30"):
        adapter.validate_content(content)


def test_douyin_adapter_content_limit() -> None:
    """测试抖音内容限制验证。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="标题",
        content="A" * 301,
        tags=[],
    )
    with pytest.raises(ValidationError):
        adapter.validate_content(content)


def test_douyin_adapter_too_many_tags() -> None:
    """测试抖音标签数量超限。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    tags = [f"tag{i}" for i in range(16)]
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="标题",
        content="内容",
        tags=tags,
    )
    with pytest.raises(ValidationError, match="15"):
        adapter.validate_content(content)


@pytest.mark.asyncio
async def test_douyin_publish_mock() -> None:
    """测试抖音发布（模拟）。"""
    from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter

    adapter = DouyinPlatformAdapter()
    content = AdaptedContent(
        platform="douyin",
        platform_name="抖音",
        title="短视频",
        content="口播脚本",
        tags=["热门"],
    )
    result = await adapter.publish(content, draft=True)
    assert "id" in result or "status" in result


# ─── 通用测试 ───


@pytest.mark.parametrize("platform_id", list(PLATFORM_ADAPTERS.keys()))
def test_all_adapters_instantiate(platform_id: str) -> None:
    """测试所有适配器都能正常实例化。"""
    adapter = get_adapter(platform_id)
    assert adapter.platform_id == platform_id
    assert adapter.platform_name  # 非空


@pytest.mark.parametrize("platform_id", list(PLATFORM_ADAPTERS.keys()))
def test_all_adapters_get_info(platform_id: str) -> None:
    """测试所有适配器都能返回平台信息。"""
    adapter = get_adapter(platform_id)
    info = adapter.get_platform_info()
    assert "platform_id" in info
    assert "platform_name" in info
    assert info["platform_id"] == platform_id
