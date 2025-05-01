from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta = PluginMetadata(
    name="cheat",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from .orm import *
from .call import *