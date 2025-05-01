from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="runManager",
	description="",
	usage="",
	config=Config,
)

from .runManager import *