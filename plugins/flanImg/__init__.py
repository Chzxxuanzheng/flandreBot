from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta = PluginMetadata(
    name="flanImg",
    description="芙兰图",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from .flanImg import *