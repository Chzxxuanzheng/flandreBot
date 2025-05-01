from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="logReport",
	description="",
	usage="",
	config=Config,
)

from .logReport import *