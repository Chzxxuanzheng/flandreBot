from typing import Type
from nonebot import on_message
from .matchers import matcherMakerFactory, Matcher

def __on_message(*args, **kwargs)-> Type[Matcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_message(_depth=_depth+1, *args, **kwargs) # type: ignore
	matcher.__name__ = 'MsgMatcher'
	return matcher


messageMatcher = matcherMakerFactory(__on_message)