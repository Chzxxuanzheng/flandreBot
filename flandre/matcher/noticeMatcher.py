from typing import Type
from nonebot import on_notice
from .matchers import matcherMakerFactory, Matcher

def __on_notice(*args, **kwargs)-> Type[Matcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_notice(_depth=_depth+1, *args, **kwargs) # type: ignore
	matcher.__name__ = 'NoticeMatcher'
	return matcher


noticeMatcher = matcherMakerFactory(__on_notice)