from nonebot import get_driver, logger
from nonebot.adapters import Event

from corePlugins.pluginsLoad.repeat import getPluginLoadReport, DisablePlugin

from core.matcher import connectMatcher
from .config import config

driverConfig = get_driver().config

@connectMatcher(msgType='private', id=driverConfig.superusers, desc='开机信息')
async def online():
	logger.info(f"发送开机信息: {config.info}")
	yield config.info
	yield str(getPluginLoadReport())