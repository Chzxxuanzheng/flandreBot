from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
	"""Plugin Config Here"""
	pluginsPath: str
	testPluginsPath: str = ''
	testDisablePlugins: list[str] = []
	isProd: bool

config = get_plugin_config(Config)