from .matchers import matcherMakerFactory, on, Matcher
from nonebot_plugin_uninfo import SupportScope
from nonebot.rule import Rule


def __on_connect(scope: str|SupportScope, **kwargs)-> type[Matcher]:
	from flandre.event import ConnectEvent
	if isinstance(scope, str):
		scope = SupportScope(scope)

	async def isPlatform(event: ConnectEvent) -> bool:
		"""检查事件的 platform 是否匹配"""
		return event.scope == scope

	_depth: int = kwargs.pop('_depth', 0)
	matcher = on(
		type = "meta_event",
		temp = True,
		_depth = _depth+1, # type: ignore

		rule = Rule(isPlatform) & kwargs.pop('rule', None),
		permission = kwargs.pop('permission', None),
		handlers = kwargs.pop('handlers', None),
		expire_time = kwargs.pop('expire_time', None),
		priority = kwargs.pop('priority', 1),
		state = kwargs.pop('state', None),
		block = kwargs.pop('block', False),

		**kwargs,
	)
	matcher.__name__ = 'ConnectMatcher'
	return matcher

connectMatcher = matcherMakerFactory(__on_connect)