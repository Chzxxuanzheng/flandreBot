# 借鉴于 https://github.com/ElainaFanBoy/nonebot_plugin_githubcard

from nonebot.plugin import PluginMetadata

from .config import Config, config

__plugin_meta__ = PluginMetadata(
	name="githubCard",
	description="",
	usage="",
	config=Config,
)

from .githubCard import *