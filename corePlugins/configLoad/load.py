from nonebot.log import logger, default_format
from nonebot import get_driver
from nonebot.config import Config

from collections.abc import Mapping
from toml import load
import os

def mergeConfig(*cfgs: Mapping) -> Mapping:
	"""
	合并配置文件, 越靠后优先级越高
	:param cfgs: 配置文件
	:return: 合并后的配置文件
	"""
	if len(cfgs) == 1:return cfgs[0]
	cfg = cfgs[0]
	for i in range(1, len(cfgs)):
		cfg = merge(cfg, cfgs[i])
	return cfg

def merge(base: Mapping, override: Mapping) -> Mapping:
	"""
	递归合并两个字典，将 override 的值覆盖到 base 上。
	"""
	for key, value in override.items():
		if isinstance(value, Mapping) and key in base and isinstance(base[key], Mapping):
			base[key] = mergeConfig(base[key], value)
		else:
			base[key] = value
	return base


os.environ.setdefault('ENVIRONMENT', 'dev')
__ENVIRONMENT = os.environ['ENVIRONMENT']
if __ENVIRONMENT == 'prod':
	IS_PROD = True
else:
	IS_PROD = False


logger.info('==================================')
if IS_PROD:
	logger.info('在生产环境下运行')
else:
	logger.warning('在测试环境下运行')
logger.info('==================================')


if IS_PROD:
	logger.add("./log/error.log", level="WARNING", format=default_format, rotation="1 week")
	import builtins
	def _print(*args, **kwargs): raise RuntimeError("在生产环境下禁止使用print")
	builtins.print = _print

def __loadConfig():
	config = load('config.toml')
	main = config.pop('flandre')
	test = config.pop('test')
	if IS_PROD: test = {}
	return mergeConfig(main, config, test)

__config = __loadConfig()
__config['isProd'] = IS_PROD
__config['env'] = __ENVIRONMENT

get_driver().config = Config(**__config)