from nonebot import get_driver, logger

from flandre.pluginsLoader.report import getPluginLoadReport

from flandre import connectMatcher, target
from .config import config

driverConfig = get_driver().config

@connectMatcher('QQClient', desc='开机信息')
async def online():
	logger.info(f"发送开机信息: {config.info}")
	for i in driverConfig.superusers:
		yield target('private', i)
		yield config.info
		yield str(getPluginLoadReport())