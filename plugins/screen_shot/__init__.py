from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="screen_shot",
	description="",
	usage="",
	config=Config,
)

from .screen_shot import *