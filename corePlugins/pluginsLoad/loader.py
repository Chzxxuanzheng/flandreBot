from nonebot import load_plugins, logger

from .config import config
from .repeat import getPluginLoadReport

if not config.pluginsPath:
	logger.opt(colors=True).warning("<y>未设置pluginsPath</y>，将不会加载任何插件")
else: load_plugins(config.pluginsPath)  # 生产插件
# 生产环境
if not config.isProd:
	# 测试插件
	if config.testPluginsPath:
		load_plugins(config.testPluginsPath)
getPluginLoadReport().repeat()  # 汇报插件加载情况