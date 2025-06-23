from nonebot.adapters import Message, Event, Bot
from nonebot.matcher import Matcher
from pydantic import ConfigDict
from typing import override, Type, ClassVar, TypeVar
from inspect import isabstract

FINAL_EVENT: list[Type['BaseEvent']] = []

TE = TypeVar('TE', bound='BaseEvent')
def finalEvent(cls: Type[TE]) -> Type[TE]:
	if isabstract(cls):
		raise ValueError(f'Cannot register abstract class {cls.__name__} as final event.')
	FINAL_EVENT.append(cls)
	return cls

class BaseEvent(Event):
	model_config = ConfigDict(arbitrary_types_allowed=True)

	__type__: ClassVar[str]
	__event_name__: ClassVar[str]

	__log_level__: ClassVar[str]
	__support_uninfo__: ClassVar[bool]
	__dont_report_error__: ClassVar[bool]

	@override
	def get_type(self) -> str:
		return self.__type__
	
	@override
	def get_event_name(self) -> str:
		"""获取事件名称的方法。"""
		return f'{self.__type__}:{self.__event_name__}'

	@override
	def get_message(self) -> Message:
		raise ValueError("Event has no message!")

	@override
	def get_user_id(self) -> str:
		raise ValueError("Event has no user id!")

	@override
	def get_session_id(self) -> str:
		raise ValueError("Event has no sesson id!")

	@override
	def is_tome(self) -> bool:
		return False


@finalEvent
class MatcherErrorEvent(BaseEvent):
	"""
	错误事件
	"""
	__type__ = 'meta_event'
	__event_name__ = 'err'

	__dont_report_error__ = True

	matcher: Matcher
	event: Event
	error: Exception

	@override
	def get_event_description(self) -> str:
		"""获取事件描述的方法，通常为事件具体内容。"""
		return f'run <y>{self.matcher}</y> failed with <r> {self.error} </r> when handling event <c>{self.event}</c>'


@finalEvent
class ConnectEvent(BaseEvent):
	"""
	连接协议层事件
	"""
	__type__ = 'meta_event'
	__event_name__ = 'connect'

	self_id: str
	adapter: 'SupportAdapter'
	scope: 'SupportScope'

	@override
	def get_event_description(self) -> str:
		return f'connected to <blue>{self.self_id}</blue> on <green>{self.adapter}</green>(<yellow>{self.scope}</yellow>)'
	

@finalEvent
class TimeEvent(BaseEvent):
	"""
	定时任务
	"""
	__type__ = 'meta_event'
	__event_name__ = 'timer'
	id: str

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cornArgs = [
			'second',
			'minute',
			'hour',
			'day',
			'day_of_week',
			'week',
			'month',
			'year',
			'start_date',
			'end_date',
		]
		intervalArgs = [
			'seconds',
			'minutes',
			'hours',
			'days',
			'months',
			'years',
			'start_date',
			'end_date',
		]
		type = kwargs.get('trigger', None)
		if type not in ['cron', 'interval']:
			raise ValueError('trigger must be cron or interval')
		self.argDesc = ''
		if type == 'cron':
			for i in cornArgs:
				if i in kwargs.keys():
					self.argDesc += f'{i}={kwargs[i]}, '
			self.descStr = f'cron event triggered with {self.argDesc}'
		elif type == 'interval':
			for i in intervalArgs:
				if i in kwargs.keys():
					self.argDesc += f'{i}={kwargs[i]}, '
			self.descStr = f'interval event triggered every {self.argDesc}'

	@override
	def get_event_description(self) -> str:
		return f'{self.descStr}'





# uninfo适配
from nonebot_plugin_uninfo import SupportScope, SupportAdapter
from nonebot_plugin_uninfo.adapters import INFO_FETCHER_MAPPING
supportUninfoEvent = [i for i in FINAL_EVENT if getattr(i, '__support_uninfo__', False)]
globals().update({'SupportScope':SupportScope, 'SupportAdapter':SupportAdapter})
for _, fetch in INFO_FETCHER_MAPPING.items(): # type: ignore
	for eventType in supportUninfoEvent:
		if not hasattr(eventType, 'uninfoSupply'):
			raise ValueError(f'Event {eventType.__name__} is marked support uninfo, but does not have uninfoSupply method!')
		fetch.supply(eventType.uninfoSupply) # type: ignore


# 事件注册
from nonebot import get_driver
from nonebot.message import run_postprocessor
from nonebot.adapters import Bot

driver = get_driver()

@driver.on_startup
def _():
	from .annotated import BasicInfo
	@driver.on_bot_connect
	async def registerConnectEvent(bot: Bot, info: BasicInfo):
		backendHandOutEvent(bot, ConnectEvent(
			self_id=info.self_id,
			adapter=info.adapter,
			scope=info.scope,
		))


	@run_postprocessor
	async def registerErrorEvent(bot: Bot, event: Event, matcher: Matcher, exception: Exception|None):
		if not exception:return
		if getattr(event, '_DO_NOT_REPORT_ERROR', False):return
		backendHandOutEvent(bot, MatcherErrorEvent(
			matcher=matcher,
			event=event,
			error=exception
		))



# 事件分发

from nonebot import logger
from nonebot.rule import TrieRule
from nonebot.utils import escape_tag, run_coro_with_shield
from nonebot.exception import NoLogException, StopPropagation
from nonebot.typing import T_DependencyCache
from nonebot.message import (
	_apply_event_postprocessors,
	_apply_event_preprocessors,
	_handle_exception,
	check_and_run_matcher,
)
from nonebot.internal.matcher import matchers

import anyio
from exceptiongroup import BaseExceptionGroup, catch
from contextlib import AsyncExitStack
from typing import Any
import asyncio

tasks: set[asyncio.Task] = set()
async def handOutEvent(source: Bot|str, event: Event):
	'''向Matchers分发事件 类似nonebot.message.handle_event

	如果事件来自于bot,source为该bot。否则source为事件来源的字符串描述。

	如果你需要非阻塞式同步函数执行事件，请使用 *backendHandOutEvent* ，使用本函数请使用await阻塞式，或者自行处理任务退出。

    参数:
        source: Bot 对象 或 str
        event: Event 对象
	'''
	show_log = True
	if isinstance(source, str):
		bot = None
		log_msg = f"<m>{source}</m> | "
	elif isinstance(source, Bot):
		bot = source
		log_msg = f"<m>{escape_tag(bot.type)} {escape_tag(bot.self_id)}</m> | "
	else:
		raise ValueError("No bot or source provided for event logging.")
	try:
		log_msg += event.get_log_string()
	except NoLogException:
		show_log = False
	if show_log:
		logger.opt(colors=True).success(log_msg)

	state: dict[Any, Any] = {}
	dependency_cache: T_DependencyCache = {}

	# create event scope context
	async with AsyncExitStack() as stack:
		if not await _apply_event_preprocessors(
			bot=bot, # type: ignore
			event=event,
			state=state,
			stack=stack,
			dependency_cache=dependency_cache,
		):
			return

		# Trie Match
		try:
			TrieRule.get_value(bot, event, state) # type: ignore
		except Exception as e:
			logger.opt(colors=True, exception=e).warning(
				"Error while parsing command for event"
			)

		break_flag = False

		def _handle_stop_propagation(exc_group: BaseExceptionGroup) -> None:
			nonlocal break_flag

			break_flag = True
			logger.debug("Stop event propagation")

		# iterate through all priority until stop propagation
		for priority in sorted(matchers.keys()):
			if break_flag:
				break

			if show_log:
				logger.debug(f"Checking for matchers in priority {priority}...")

			if not (priority_matchers := matchers[priority]):
				continue

			with catch(
				{
					StopPropagation: _handle_stop_propagation,
					Exception: _handle_exception(
						"<r><bg #f8bbd0>Error when checking Matcher.</bg #f8bbd0></r>"
					),
				}
			):
				async with anyio.create_task_group() as tg:
					for matcher in priority_matchers:
						tg.start_soon(
							run_coro_with_shield,
							check_and_run_matcher(
								matcher,
								bot, # type: ignore
								event,
								state.copy(),
								stack,
								dependency_cache,
							),
						)

		if show_log:
			logger.debug("Checking for matchers completed")

		await _apply_event_postprocessors(bot, event, state, stack, dependency_cache) # type: ignore


def backendHandOutEvent(source: Bot|str, event: Event):
	'''向Matchers分发事件 类似nonebot.message.handle_event

	如果事件来自于bot,source为该bot。否则source为事件来源的字符串描述。

	如果你需要阻塞式运行，其使用`await handOutEvent(source, event)`。

    参数:
        source: Bot 对象 或 str
        event: Event 对象
	'''
	task = asyncio.create_task(handOutEvent(source, event))
	task.add_done_callback(tasks.discard)
	tasks.add(task)

@driver.on_shutdown
async def stop():
	for task in tasks:
		if not task.done():
			task.cancel()

	await asyncio.gather(
		*(asyncio.wait_for(task, timeout=10) for task in tasks),
		return_exceptions=True,
	)