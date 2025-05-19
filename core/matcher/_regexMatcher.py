from ._matchers import ExMatcher, passiveMatcherMake
from nonebot import on_regex

def __on_regex(*args, **kwargs)-> type[ExMatcher]:
	# 创建一个正则表达式Matcher，支持命令别名
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on_regex(*args, _depth=_depth+1, **kwargs)
	matcher.__name__ = 'RegexMatcher'
	return matcher

regexMatcher = passiveMatcherMake(__on_regex)