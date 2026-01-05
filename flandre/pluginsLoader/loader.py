from nonebot import load_plugins, logger, load_plugin

from .config import config
from .report import getPluginLoadReport

def loadPluginsFromConfig():
	if not config.pluginsPath:
		logger.opt(colors=True).warning("<y>未设置pluginsPath</y>，生产环境下将不会加载任何插件")
	else:
		logger.opt(colors=True).info(f"正在加载<g>生产环境</g>插件目录: {config.pluginsPath}")
		load_plugins(config.pluginsPath)  # 生产插件
	# 生产环境
	if not config.isProd:
		# 测试插件
		if config.testPluginsPath:
			logger.opt(colors=True).info(f"正在加载<y>测试环境</y>插件目录: {config.testPluginsPath}")
			load_plugins(config.testPluginsPath)
	getPluginLoadReport().report()  # 汇报插件加载情况