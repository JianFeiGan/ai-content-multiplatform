"""平台适配器模块。"""

from ai_content_multiplatform.platforms.base import BasePlatformAdapter
from ai_content_multiplatform.platforms.csdn import CSDNPlatformAdapter
from ai_content_multiplatform.platforms.douyin import DouyinPlatformAdapter
from ai_content_multiplatform.platforms.juejin import JuejinPlatformAdapter
from ai_content_multiplatform.platforms.toutiao import ToutiaoPlatformAdapter
from ai_content_multiplatform.platforms.weixin import WeixinPlatformAdapter
from ai_content_multiplatform.platforms.xiaohongshu import XiaohongshuPlatformAdapter
from ai_content_multiplatform.platforms.zhihu import ZhihuPlatformAdapter

# 平台适配器注册表
PLATFORM_ADAPTERS: dict[str, type[BasePlatformAdapter]] = {
    "weixin": WeixinPlatformAdapter,
    "zhihu": ZhihuPlatformAdapter,
    "csdn": CSDNPlatformAdapter,
    "douyin": DouyinPlatformAdapter,
    "xiaohongshu": XiaohongshuPlatformAdapter,
    "juejin": JuejinPlatformAdapter,
    "toutiao": ToutiaoPlatformAdapter,
}


def get_adapter(platform_id: str) -> BasePlatformAdapter:
    """获取平台适配器实例。

    Args:
        platform_id: 平台标识。

    Returns:
        平台适配器实例。

    Raises:
        ValueError: 当平台不支持时抛出。
    """
    if platform_id not in PLATFORM_ADAPTERS:
        raise ValueError(
            f"不支持的平台: {platform_id}，"
            f"可选: {', '.join(PLATFORM_ADAPTERS.keys())}"
        )
    return PLATFORM_ADAPTERS[platform_id]()
