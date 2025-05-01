from pydantic import BaseModel, ConfigDict, AliasPath, AliasGenerator
from nonebot import get_plugin_config
from typing import Self

__pluginNameCache = []

class __BaseConfig(BaseModel):
	@classmethod
	def getConfig(cls)->Self:
		return get_plugin_config(cls)

def baseConfig(name: str) -> __BaseConfig:
	if name in __pluginNameCache:
		raise Exception(f'插件{name}重复')
	__pluginNameCache.append(name)
	class Config(__BaseConfig):
		model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=lambda field_name: AliasPath(name, field_name)))
	return Config