from ._matchers import on_emit, ExMatcher, activeMatcherMake
from typing import Type
from core.event import MatcherErrorEvent
from core.target import Target
from nonebot.message import handle_event, run_postprocessor
from nonebot.adapters import Event, Bot
from typing import Optional
from asyncio.taskgroups import TaskGroup

__eventList: Type[MatcherErrorEvent] = []

@run_postprocessor
async def _(bot: Bot, event: Event, matcher: ExMatcher, exception: Optional[Exception]):
	if not exception:return
	if isinstance(event, MatcherErrorEvent):return
	async with TaskGroup() as group:
		for eventType in __eventList:
			group.create_task(handle_event(bot, eventType(event=event, errMatcher=matcher, error=exception)))

def __matcherErrorEmitEvent(args, kwargs)-> None:
	matcher: Type[ExMatcher] = kwargs.pop('matcher')
	type: str = kwargs.pop('msgType')
	id: str|list[str] = kwargs.pop('id')
	class _MatcherErrorEvent(MatcherErrorEvent):
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs, matcher=matcher, target=Target(type, id))

	__eventList.append(_MatcherErrorEvent)

def __on_error(*args, **kwargs)-> type[ExMatcher]:
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
	matcher.__name__ = 'ErrMatcher'
	return matcher

matcherErrorMatcher = activeMatcherMake(__on_error, __matcherErrorEmitEvent)