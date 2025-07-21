from nonebot.typing import T_Handler, T_State
from nonebot.adapters import Bot
from nonebot.internal.matcher import current_event, current_bot
from nonebot_plugin_alconna.uniseg import Target, SupportScope
from nonebot_plugin_uninfo import Session, get_session
from typing import Callable, Literal, Type, Iterable, TYPE_CHECKING
from functools import wraps
from nonebot import on as on

from flandre.annotated import current_di_arg
from flandre.typing import T_DIArg
from .sender import createSender, Sender

if TYPE_CHECKING:
	from flandre.init.patchs import PatchMatcher as Matcher
else:
	from nonebot.matcher import Matcher

type MatcherMaker = Callable[..., type[Matcher]]
type MatcherDecoratorMaker = Callable[..., MatcherDecorator]
type MatcherDecorator = Callable[..., T_Handler]
type EmitEventFunc = Callable[..., None]
type SenderMaker = Callable[[Bot, int|str|Iterable[int|str]], Sender]
type SenderMakerFactory = Callable[..., SenderMaker]

def matcherMakerFactory(matcherMaker: MatcherMaker)-> MatcherDecoratorMaker:
	"""主动消息处理器生成器
	
	Keyword arguments:
	matcherMaker -- 生成Matcher的函数
	emitEventFunc -- 委托事件处理函数
	Return: 封装好的matcher装饰器
	"""

	# 生成一个装饰器函数，用于创建Matcher并处理消息
	def func(*args, **kwargs)-> MatcherDecorator:
		# 生成defaultTarget
		defaultTarget = None
		if 'defaultTarget' in kwargs:
			defaultTarget = kwargs.pop('defaultTarget')
		elif 'msgType' in kwargs or 'id' in kwargs:
			if not ('msgType' in kwargs and 'id' in kwargs):
				raise ValueError('Matcher必须同时提供msgType和id')
			
			defaultTarget = target(kwargs.pop('msgType'), kwargs.pop('id'), kwargs.pop('platform', None))
		kwargs['defaultTarget'] = defaultTarget

		# 创建Matcher
		matcher: Type[Matcher] = matcherMaker(*args,**kwargs, _depth=1)

		sender: Sender|None = None

		# 连接Matcher，并根据消息类型和ID发送消息
		def decorator(func: T_Handler)-> T_Handler:
			# 创建sender
			@matcher.handle()
			async def info(state: T_State):
				nonlocal sender
				bot = current_bot.get()
				event = current_event.get()
				current_di_arg.set(T_DIArg(bot=bot, event=event, state=state))
				defaultTarget = None
				try:
					session: Session|None = await get_session(bot, event)
				except Exception as e:
					session = None
				if matcher.defaultTarget:
					defaultTarget = matcher.defaultTarget
				elif session:
					defaultTarget = getTargetFromSession(session)
				else:
					defaultTarget = None
				sender = createSender(defaultTarget)
			@matcher.handle()
			@wraps(func)
			async def handle(*args, **kwargs):
				await sender(func, *args, **kwargs) # type: ignore
			return func
		return decorator
	return func

def getTargetFromSession(session: Session):
	if session.scope == SupportScope.minecraft:return Target.group('0', session.scope)
	if session.group:
		return Target.group(session.group.id, session.scope)
	else:
		return Target.user(session.user.id, session.scope)

def target(msgType: Literal['group', 'private'], id: str|int, platform: str|None=None)-> Target:
	if platform is None:
		platform = SupportScope.qq_client
	elif isinstance(platform, str):
		platform = SupportScope(platform)
	if msgType == 'group':
		return Target.group(str(id), platform)
	elif msgType == 'private':
		return Target.user(str(id), platform)
	else:
		raise ValueError('msgType must be "group" or "private"')