from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
    name="onlineInfo",
    description="开机信息",
    usage="",
    config=Config,
)

from .run import *