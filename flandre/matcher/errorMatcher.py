from .matchers import on, Matcher, matcherMakerFactory
from nonebot.rule import Rule
from nonebot.adapters import Event

def __isErrEventFunc(event: Event) -> bool:
	from flandre.event import MatcherErrorEvent
	return isinstance(event, MatcherErrorEvent)

__isErrEvent = Rule(__isErrEventFunc)

def __on_error(*args, **kwargs)-> type[Matcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on(
		type = "meta_event",
		_depth = _depth+1, # type: ignore
		rule = __isErrEvent & kwargs.pop('rule', None),
		permission = kwargs.pop('permission', None),
		handlers = kwargs.pop('handlers', None),
		expire_time = kwargs.pop('expire_time', None),
		priority = kwargs.pop('priority', 1),
		state = kwargs.pop('state', None),
		block = kwargs.pop('block', False),
		temp = kwargs.pop('temp', False),
		**kwargs
	)
	matcher.__name__ = 'ErrMatcher'
	return matcher

matcherErrorMatcher = matcherMakerFactory(__on_error)