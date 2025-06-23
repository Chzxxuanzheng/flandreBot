from typing import Literal, TypedDict
from contextlib import AsyncExitStack

from nonebot.typing import T_State, T_DependencyCache
from nonebot.adapters import Bot, Event

type ScopeLiteral = Literal[
	'QQClient',
	'QQGuild',
	'QQAPI',
	'Telegram',
	'Discord',
	'Feishu',
	'DoDo',
	'Heybox',
	'Kaiheila',
	'Mail',
	'Minecraft',
	'GitHub',
	'Console',
	'Ding',
	'WeChat',
	'WeChatOfficialAccountPlatform',
	'WeCom',
	'TailChat',
	'Onebot12',
	'satori',
]

type logLevel = Literal[
	'none',
	'debug',
	'scuess',
	'info',
	'warning',
	'error',
	'critical',
]

class T_DIArg(TypedDict):
	"""依赖注入必须参数"""
	bot: Bot|None
	event: Event
	state: T_State
	# stack: AsyncExitStack
	# dependency_cache: T_DependencyCache