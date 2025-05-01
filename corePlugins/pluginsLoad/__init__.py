from nonebot import require
require('corePlugins.configLoad')
from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
    name="pluginsLoad",
    description="",
    usage="",
    config=Config,
)

from .loader import *