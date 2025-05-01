from nonebot import on_message, on, get_driver
from nonebot.message import handle_event
from nonebot.rule import Rule
from nonebot.typing import T_Handler
from nonebot.adapters import Bot, Event
from core.event import *
from typing import Callable, Any, Type, Iterable
from functools import wraps
from .exMatcher import ExMatcher

from ._sender import createSender, Sender

type MatcherMaker = Callable[[Any], type[ExMatcher]]
type MatcherDecoratorMaker = Callable[[Any], MatcherDecorator]
type MatcherDecorator = Callable[[Any], T_Handler]
type EmitEventFunc = Callable[[Any], None]
type SenderMaker = Callable[[Bot, int|str|Iterable[int|str]], Sender]
type SenderMakerFactory = Callable[[Any], SenderMaker]


def activeMatcherMake(matcherMaker: MatcherMaker, emitEventFunc: EmitEventFunc)-> MatcherDecoratorMaker:
	"""主动消息处理器生成器
	
	Keyword arguments:
	matcherMaker -- 生成Matcher的函数
	emitEventFunc -- 委托事件处理函数
	Return: 封装好的matcher装饰器
	"""

	# 生成一个装饰器函数，用于创建Matcher并处理消息
	def func(*args, **kwargs)-> MatcherDecorator:
		desc = kwargs.pop('desc', None)
		if not desc:
			raise ValueError('Matcher必须提供描述信息')
		# 创建Matcher
		match: Type[ExMatcher] = matcherMaker(*args,**kwargs, _depth=1)
		match.desc = desc

		kwargs['matcher'] = match
		emitEventFunc(args, kwargs)

		sender: Sender = None

		# 连接Matcher，并根据消息类型和ID发送消息
		def decorator(func: T_Handler)-> T_Handler:
			# 创建sender
			@match.handle()
			async def info(bot: Bot, event: Event):
				nonlocal sender
				sender = createSender(bot, event)
			@match.handle()
			@wraps(func)
			async def handle(*args, **kwargs):
				await sender(func, *args, **kwargs)
			return func
		return decorator
	return func

def passiveMatcherMake(matcherMaker: MatcherMaker)-> MatcherDecoratorMaker:
	"""主动消息处理器生成器
	
	Keyword arguments:
	matcherMaker -- 生成Matcher的函数
	Return: 封装好的matcher装饰器
	"""
	return activeMatcherMake(matcherMaker, lambda args, kwargs: kwargs.pop('matcher'))

def on_emit(*args, **kwargs)-> type[ExMatcher]:
	_depth: int = kwargs.pop('_depth', 0)
	matcher = on(_depth = _depth+1, *args, **kwargs)
	async def emitCheck(event: EmitEvent)-> bool:
		nonlocal matcher
		return event.matcher == matcher
	matcher.rule = Rule(emitCheck) & matcher.rule
	return matcher
