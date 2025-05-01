from ._matchers import on_emit, ExMatcher, activeMatcherMake
from typing import Type
from core.event import TimeEvent
from core.target import Target
from nonebot import get_driver
from nonebot.message import handle_event
from nonebot.adapters import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class __Schedule(AsyncIOScheduler):
	def __init__(self):
		super().__init__()
		self.bot: Bot = None

	def start(self, bot: Bot):
		self.bot = bot
		super().start()

	def addJob(self, **kwargs):
		EventType: Type[TimeEvent] = kwargs.pop('eventType')
		async def createEvent():
			await handle_event(self.bot, EventType())
		self.add_job(createEvent, **kwargs)
		

__scheduler = __Schedule()


@get_driver().on_bot_connect
async def _(bot: Bot):
	if not __scheduler.running:
		__scheduler.start(bot)


get_driver().on_shutdown(__scheduler.shutdown)


def __timeEmitEvent(args, kwargs)-> None:
	matcher: Type[ExMatcher] = kwargs.pop('matcher')
	type: str = kwargs.pop('msgType')
	id: str|list[str] = kwargs.pop('id')
	class _TimeEvent(TimeEvent):
		def __init__(self):
			super().__init__(*args, **kwargs, matcher = matcher, target=Target(type, id))

	__scheduler.addJob(eventType = _TimeEvent, **kwargs)

def __on_timer(*args, **kwargs)-> type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_emit(
		type = "meta_event",
		_depth = _depth+1,
		rule = kwargs.pop('rule', None),
		permission = kwargs.pop('permission', None),
		handlers = kwargs.pop('handlers', None),
		expire_time = kwargs.pop('expire_time', None),
		priority = kwargs.pop('priority', 1),
		state = kwargs.pop('state', None),
		block = kwargs.pop('block', False),
		temp = kwargs.pop('temp', False),
	)
	matcher.__name__ = 'TimMatcher'
	return matcher

timerMatcher = activeMatcherMake(__on_timer, __timeEmitEvent)

def cronMatcher(*args, **kwargs)-> type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	return timerMatcher(*args, **kwargs, trigger = "cron")

def intervalMatcher(*args, **kwargs)-> type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	return timerMatcher(*args, **kwargs, trigger = "interval")