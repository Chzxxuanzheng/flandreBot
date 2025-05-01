from ._matchers import ExMatcher, on_emit, activeMatcherMake
from nonebot.message import handle_event
from nonebot.adapters import Bot
from nonebot.drivers import Driver
from nonebot import get_driver
from core.event import ConnectEvent
from core.target import Target
from datetime import datetime
from typing import Type
from asyncio.taskgroups import TaskGroup

__eventList = []

def __connectEmitEvent(args, kwargs)-> None:
	matcher: Type[ExMatcher] = kwargs.pop('matcher')
	type: str = kwargs.pop('msgType')
	id: str|list[str] = kwargs.pop('id')
	class _ConnectEvent(ConnectEvent):
		def __init__(self, driver: Driver, time: datetime):
			super().__init__(driver, time, *args, **kwargs, matcher = matcher, target=Target(type, id))
	__eventList.append(_ConnectEvent)

def __on_connect(*args, **kwargs)-> type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_emit(
		type = "meta_event",
		temp = True,
		_depth = _depth+1,

		rule = kwargs.pop('rule', None),
		permission = kwargs.pop('permission', None),
		handlers = kwargs.pop('handlers', None),
		expire_time = kwargs.pop('expire_time', None),
		priority = kwargs.pop('priority', 1),
		state = kwargs.pop('state', None),
		block = kwargs.pop('block', False),
	)
	matcher.__name__ = 'ConMatcher'
	return matcher

connectMatcher = activeMatcherMake(__on_connect, __connectEmitEvent)

__driver = get_driver()
@__driver.on_bot_connect
async def _(bot: Bot):
	events = [event(bot, datetime.now()) for event in __eventList]
	async with TaskGroup() as g:
		for event in events:
			g.create_task(handle_event(bot, event))