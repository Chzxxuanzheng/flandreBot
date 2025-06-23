from pydantic import BaseModel, ConfigDict, AliasPath, AliasGenerator
from nonebot import get_plugin_config
from typing import Self, Type

__pluginNameCache = []

class BaseConfig(BaseModel):
	@classmethod
	def getConfig(cls)->Self:
		return get_plugin_config(cls)

def baseConfig(name: str) -> Type[BaseConfig]:
	if name in __pluginNameCache:
		raise Exception(f'插件{name}重复')
	__pluginNameCache.append(name)
	class Config(BaseConfig):
		model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=lambda field_name: AliasPath(name, field_name)))
	return Config

class Config(BaseModel):
	adapters: str|list[str]