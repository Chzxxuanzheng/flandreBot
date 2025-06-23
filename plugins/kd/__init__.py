from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="kd",
	description="",
	usage="",
	config=Config,
)

from .kd import *