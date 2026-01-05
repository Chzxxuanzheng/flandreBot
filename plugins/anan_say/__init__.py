from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="anan_say",
	description="",
	usage="",
	config=Config,
)

from .anan_say import *