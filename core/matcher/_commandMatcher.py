from ._matchers import ExMatcher, passiveMatcherMake
from nonebot import on_command
from util.rule import norRule

def __on_command(*args, **kwargs)-> type[ExMatcher]:
	rule = kwargs.pop('rule', norRule)
	# 创建一个命令Matcher，支持命令别名
	kwargs.setdefault('block', True)
	_depth: int = kwargs.pop('_depth', 0)
	alias = args[1:]
	com = args[0]
	matcher = on_command(com, aliases=set(alias), rule=rule, _depth=_depth+1, **kwargs)
	matcher.__name__ = 'CmdMatcher'
	return matcher

commandMatcher = passiveMatcherMake(__on_command)