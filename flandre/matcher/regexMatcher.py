from .matchers import Matcher, matcherMakerFactory
from nonebot import on_regex

def __on_regex(*args, **kwargs)-> type[Matcher]:
	# 创建一个正则表达式Matcher，支持命令别名
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_regex(*args, _depth=_depth+1, **kwargs) # type: ignore
	matcher.__name__ = 'RegexMatcher'
	return matcher

regexMatcher = matcherMakerFactory(__on_regex)