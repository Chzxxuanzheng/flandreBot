from .message import toPlaintext

from nonebot.typing import T_State
from nonebot.params import Depends, _command_arg
from nonebot.adapters import Bot, Event

from typing import Any, Annotated, Callable
from dataclasses import dataclass

from nonebot_plugin_alconna.uniseg import Text, UniMsg, UniMessage
from nonebot_plugin_uninfo import Session, get_session, SupportAdapter, SupportScope, QryItrface, Member
from nonebot_plugin_uninfo.adapters import INFO_FETCHER_MAPPING

@dataclass
class _BasicInfo:
    self_id: str
    adapter: SupportAdapter
    scope: SupportScope


from flandre.event import BaseEvent as CustomEvent

async def _uninfo(bot: Bot, event: Event)->None|Session:
	if isinstance(event, CustomEvent):
		if not getattr(event, '__support_uninfo__', False):return
	return await get_session(bot, event)

Uninfo = Annotated[Session, Depends(_uninfo)]
'''对 nonebot_plugin_uninfo Uninfo依赖注入的封装，可以过滤掉不匹配的事件'''


def _basicInfo(bot: Bot) -> _BasicInfo|None:
	adapter = bot.adapter.get_name()
	fetcher = INFO_FETCHER_MAPPING.get(adapter)
	assert fetcher
	return _BasicInfo(**fetcher.supply_self(bot))


BasicInfo = Annotated[_BasicInfo, Depends(_basicInfo)]
'''对 uninfo 的封装，获取当前Bot的基本信息，包含self_id、adapter和scope'''


def _plaintext(msg: UniMsg) -> str:
	return toPlaintext(msg)


def plaintext() -> Any:
	"""获取纯文本消息"""
	return Depends(_plaintext)

def _arg(state: T_State, bot: Bot) -> UniMessage|None:
	try:
		args = _command_arg(state)
	except:
		return None
	return UniMessage.of(message=args, bot=bot)

def arg() -> Any:
	return Depends(_arg)

Arg = Annotated[UniMessage, Depends(_arg)]
"""获取指令Matcher参数，返回一个 UniMessage 对象 """

def _plaintextArg(arg: Arg) -> str|None:
	"""获取指令Matcher参数的纯文本内容"""
	data = toPlaintext(arg)
	if not data:return None
	return data

def plaintextArg() -> Any:
	"""获取指令Matcher参数的纯文本内容"""
	return Depends(_plaintextArg)

async def _tome(event: Event) -> bool:
	return event.is_tome()

def tome() -> Any:
	"""判断当前事件是否为@Bot的消息"""
	return Depends(_tome)

async def _members(interface: QryItrface, info: Uninfo) -> list[Member]|None:
	if not info.group:return
	return await interface.get_members(info.scene.type, info.group.id)

Members = Annotated[list[Member], Depends(_members)]
''' 获取当前事件所在群组的用户列表，返回一个 User 对象列表 '''

from nonebot.dependencies import Dependent
from nonebot.matcher import Matcher
from nonebot.typing import T_DependencyCache

from contextlib import AsyncExitStack
from contextvars import ContextVar
from .typing import T_DIArg

current_di_arg: ContextVar[T_DIArg] = ContextVar('current_di_arg')

def DependencyInjection() -> Callable[[Callable[..., Any]], Callable[[], Any]]:
	''' 装饰器，用于将函数转换为依赖注入函数。 '''
	def _dectory(func: Callable[..., Any]) -> Callable[[], Any]:
		dependent = Dependent[Any].parse(call=func,allow_types=Matcher.HANDLER_PARAM_TYPES)
		async def wrapper():
			await dependent(**current_di_arg.get())
		return wrapper
	return _dectory