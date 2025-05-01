from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
    name="dnfsAi",
    description="",
    usage="",
    config=Config,
)

from .ai import *
from .orm import *