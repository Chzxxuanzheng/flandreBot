from nonebot.log import logger, default_format

from toml import load
import os

type jsonData = str | int | float | bool | None | dict[str, jsonData] | list[jsonData]

def mergeConfig(*cfgs: dict[str,jsonData]) -> dict[str,jsonData]:
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

def merge(base: dict[str,jsonData], override: dict) -> dict:
	"""
	递归合并两个字典，将 override 的值覆盖到 base 上。
	"""
	for key, value in override.items():
		if isinstance(value, dict) and key in base and isinstance(base[key], dict):
			base[key] = mergeConfig(base[key], value) # type: ignore
		else:
			base[key] = value
	return base


def loadConfig(**kwargs) -> dict[str,jsonData]:
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
		logger.info('在测试环境下运行')
	logger.info('==================================')

	if IS_PROD:
		logger.add("./log/error.log", level="WARNING", format=default_format, rotation="1 week")
		import builtins
		def _print(*args, **kwargs): raise RuntimeError("在生产环境下禁止使用print")
		builtins.print = _print

	def __loadConfig():
		config = load('config.toml')
		_global = config.pop('global')
		test = config.pop('test')
		if IS_PROD: test = {}
		return mergeConfig(_global, config, test)

	config = __loadConfig()
	config['isProd'] = IS_PROD
	config['env'] = __ENVIRONMENT

	return mergeConfig(config, kwargs)