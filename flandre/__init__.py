import nonebot
from nonebot import logger
from nonebot.adapters import Adapter
import flandre.init.init as initModule
from asyncio import get_event_loop
from importlib import import_module
from typing import Any, Type, TYPE_CHECKING

from .configLoader import loadConfig
from .lock import ProcessLock
from .config import Config

def init(*adapters: Type[Adapter], **kwargs: Any):
	# 覆盖nb
	from .init import patchs as _

	# 初始化nb
	config = loadConfig(**kwargs)
	nonebot.init(**config) # type: ignore
	initModule.nowSate = initModule.InitState.AfterNbInit

	import nonebot_plugin_exdi as _

	# 注册适配器
	config = Config(**config) # type: ignore
	driver = nonebot.get_driver()
	for adapter in adapters:
		driver.register_adapter(adapter)
	if isinstance(config.adapters, str):
		configAdapters = [config.adapters]
	else:
		configAdapters = config.adapters
	for adapter in configAdapters:
		driver.register_adapter(import_module(f"nonebot.adapters.{adapter}").Adapter)

	initModule.nowSate = initModule.InitState.AfterNbInit

	# 初始化钩子
	get_event_loop().run_until_complete(initModule.runInitHook())

	initModule.nowSate = initModule.InitState.AfterInitHook

	# 加载插件
	from .pluginsLoader import loadPluginsFromConfig
	loadPluginsFromConfig()

	initModule.nowSate = initModule.InitState.AfterPluginLoader

def run(*args, **kwargs):
	if initModule.nowSate == initModule.InitState.NbNoInit:
		init()
	with ProcessLock():
		nonebot.run(*args, **kwargs)

@initModule.onInit
def _():
	from . import middleware as middleware
	from . import matcher
	globals().update({name: getattr(matcher, name) for name in dir(matcher) if not name.startswith('_')})
	from .config import baseConfig
	globals().update({'baseConfig': baseConfig})