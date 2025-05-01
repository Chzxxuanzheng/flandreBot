from nonebot import load_plugins

from .config import config
from .repeat import getPluginLoadReport

load_plugins(config.pluginsPath)  # 生产插件
# 生产环境
if not config.isProd:
	# 测试插件
	if config.testPluginsPath:
		load_plugins(config.testPluginsPath)
getPluginLoadReport().repeat()  # 汇报插件加载情况