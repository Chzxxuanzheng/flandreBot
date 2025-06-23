from .matchers import on, Matcher, matcherMakerFactory
from flandre.timer import timerManager

def __on_timer(*args, **kwargs)-> type[Matcher]:
	if args:
		raise TypeError('TimerMatcher does not accept positional arguments')
	_depth: int = kwargs.pop('_depth', 0)
	timerId: str|None = kwargs.get('desc', None)
	if timerId is None:
		raise ValueError('TimerMatcher must have a timer ID (desc)')
	rule = timerManager.registerTimeEvent(id=timerId, **kwargs) & kwargs.pop('rule', None)
	matcher = on(
		_depth = _depth + 1, # type: ignore
		rule = rule,
		**kwargs
	)
	matcher.__name__ = 'TimerMatcher'
	return matcher

timerMatcher = matcherMakerFactory(__on_timer)

def cronMatcher(*args, **kwargs)-> type[Matcher]:
	_depth: int = kwargs.pop('_depth', 0) + 1
	return timerMatcher(*args, **kwargs, trigger = "cron") # type: ignore

def intervalMatcher(*args, **kwargs)-> type[Matcher]:
	_depth: int = kwargs.pop('_depth', 0) + 1
	return timerMatcher(*args, **kwargs, trigger = "interval") # type: ignore