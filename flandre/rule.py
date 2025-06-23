from typing import Iterable

from nonebot.rule import Rule
from nonebot_plugin_uninfo import SceneType, SupportScope
from .annotated import Uninfo, BasicInfo
from .typing import ScopeLiteral


def private() -> Rule:
	'''判断是否为私聊消息'''
	async def re(session: Uninfo) -> bool:
		# 判断是否为私聊消息
		return session.scene.type == SceneType.PRIVATE
	return Rule(re)

def group() -> Rule:
	'''判断是否为群组消息'''
	async def re(session: Uninfo) -> bool:
		# 判断是否为群组消息
		return session.scene.type == SceneType.GROUP
	return Rule(re)

def users(users: Iterable[str|int]|str|int) -> Rule:
	'''
	判断消息发送者是否在指定用户列表中
	:param users: 用户列表或单个用户ID
	'''
	if isinstance(users, Iterable):
		users = [str(i) for i in users]
	else:
		users = [str(users)]
	async def re(session: Uninfo) -> bool:
		if not session: return False
		return session.user.id in users
	return Rule(re)

def groups(groups: Iterable[str|int]|str|int) -> Rule:
	'''
	判断消息所在群组是否在指定群组列表中
	:param groups: 群组列表或单个群组ID
	'''
	if isinstance(groups, Iterable):
		groups = [str(i) for i in groups]
	else:
		groups = [str(groups)]
	async def re(session: Uninfo) -> bool:
		if not session: return False
		return session.scene.id in groups
	return Rule(re)

def scope(scope: SupportScope|ScopeLiteral)-> Rule:
	if isinstance(scope, str):
		scope = SupportScope(scope)
	async def re(info: BasicInfo) -> bool:
		# 判断适配器是否匹配
		return info.scope == scope
	return Rule(re)