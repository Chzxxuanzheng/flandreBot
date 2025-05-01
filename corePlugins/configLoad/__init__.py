from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="configLoad",
    description="",
    usage="",
    config=Config,
)

from .load import *
