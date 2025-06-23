import nonebot
from typing import Optional
import nonebot.plugin
from nonebot.plugin.model import Plugin
from nonebot.utils import escape_tag
from nonebot import logger
import importlib

from .config import config

__PluginStatus: dict[str, Exception|None] = {}

class PluginLoadReport:
	def __init__(self):
		self.scuess: list[str] = []
		self.failed: list[str] = []
		self.failedResaon: dict[str, Exception] = {}
		self.ignore: list[str] = []
		self.ignoreReason: dict[str, DisablePlugin] = {}
		self.data: dict[str, Exception|None] = {}

	def record(self, name: str, reason: Exception|None):
		self.data[name] = reason
		if isinstance(reason, DisablePlugin):
			self.ignore.append(name)
			self.ignoreReason[name] = reason
		elif reason:
			self.failed.append(name)
			self.failedResaon[name] = reason
		else:
			self.scuess.append(name)

	def __str__(self):
		head = f'插件加载汇报: {len(self.scuess)}成功'
		if self.ignore:
			head += f" {len(self.ignore)}忽略"
		if self.failed:
			head += f" {len(self.failed)}失败"
		if self.ignore:
			head += f"\n忽略列表:"
		for i in self.ignore:
			head += f"\n - {i}: {self.ignoreReason[i]}"
		if self.failed:
			head += f"\n失败列表:"
		for i in self.failed:
			head += f"\n - {i}: {self.failedResaon[i]}"
		return head

	def __repr__(self):
		head = f'<y>插件加载汇报</y>: <g>{len(self.scuess)}</g>成功'
		if self.ignore:
			head += f" <y>{len(self.ignore)}</y>忽略"
		if self.failed:
			head += f" <r>{len(self.failed)}</r>失败"
		if self.ignore:
			head += f"\n<y>忽略列表</y>:"
		for i in self.ignore:
			head += f"\n <g>-</g> {i}: <y>{self.ignoreReason[i]}</y>"
		if self.failed:
			head += f"\n<r>失败列表</r>:"
		for i in self.failed:
			head += f"\n <g>-</g> {i}: <r>{self.failedResaon[i]}</r>"
		return head


	def report(self):
		logger.opt(colors=True).info(repr(self))

__reapeat = PluginLoadReport()

def loadMaker(__PluginStatus: dict[str, Exception|None]):
	def load_plugin(self, name: str) -> Optional[Plugin]:
		nonlocal __PluginStatus
		"""加载指定插件。

		可以使用完整插件模块名或者插件标识符加载。

		参数:
			name: 插件名称或插件标识符。
		"""

		try:
			# dsiable plugins at dev mod
			if not config.isProd and name in config.testDisablePlugins:
				raise DisablePlugin('测试环境禁用插件')
			# load using plugin id
			if name in self._third_party_plugin_ids:
				module = importlib.import_module(self._third_party_plugin_ids[name])
			elif name in self._searched_plugin_ids:
				module = importlib.import_module(self._searched_plugin_ids[name])
			# load using module name
			elif (
				name in self._third_party_plugin_ids.values()
				or name in self._searched_plugin_ids.values()
			):
				module = importlib.import_module(name)
			else:
				raise RuntimeError(f"Plugin not found: {name}! Check your plugin name")

			if (
				plugin := getattr(module, "__plugin__", None)
			) is None or not isinstance(plugin, Plugin):
				raise RuntimeError(
					f"Module {module.__name__} is not loaded as a plugin! "
					f"Make sure not to import it before loading."
				)
			logger.opt(colors=True).success(
				f'Succeeded to load plugin "<y>{escape_tag(plugin.id_)}</y>"'
				+ (
					f' from "<m>{escape_tag(plugin.module_name)}</m>"'
					if plugin.module_name != plugin.id_
					else ""
				)
			)
			__reapeat.record(name, None)
			return plugin
		except DisablePlugin as e:
			logger.opt(colors=True).info(
				f'Skip to load the diabled plugin "<y>{name}</y>"'
				+ f'(beacuse of "{e}")' if str(e) else ''
			)
			__reapeat.record(name, e)
		except Exception as e:
			logger.opt(colors=True, exception=e).error(
				f'<r><bg #f8bbd0>Failed to import "{escape_tag(name)}"</bg #f8bbd0></r>'
			)
			__reapeat.record(name, e)
	return load_plugin

nonebot.plugin.load.PluginManager.load_plugin = loadMaker(__PluginStatus) # type: ignore

class DisablePlugin(Exception):
	def __init__(self, resaon: str = '未知原因'):
		super().__init__(resaon)

def getPluginLoadReport()-> PluginLoadReport:
	return __reapeat
