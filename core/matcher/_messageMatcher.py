from typing import Type
from nonebot import on_message
from ._matchers import passiveMatcherMake, ExMatcher

def __on_message(*args, **kwargs)-> Type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_message(_depth=_depth+1, *args, **kwargs)
	matcher.__name__ = 'MsgMatcher'
	return matcher


messageMatcher = passiveMatcherMake(__on_message)