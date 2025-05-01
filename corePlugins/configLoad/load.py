from nonebot.log import logger, default_format
from nonebot import get_driver
from nonebot.config import Config

import yaml
from toml import load
import os

os.environ.setdefault('ENVIRONMENT', 'dev')
__ENVIRONMENT = os.environ['ENVIRONMENT']
if __ENVIRONMENT == 'prod':
	IS_PROD = True
else:
	IS_PROD = False


if IS_PROD:
	logger.add("./log/error.log", level="WARNING", format=default_format, rotation="1 week")

logger.info('==================================')
if IS_PROD:
	logger.info('在生产环境下运行')
else:
	logger.warning('在测试环境下运行')
logger.info('==================================')

def __loadConfig():
	config = load('config.toml')
	main = config.pop('flandre')
	return {**main, **config}

__config = __loadConfig()
__config['isProd'] = IS_PROD
__config['env'] = __ENVIRONMENT

get_driver().config = Config(**__config)