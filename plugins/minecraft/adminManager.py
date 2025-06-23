from nonebot import logger
from nonebot_plugin_orm import get_session, async_scoped_session
from nonebot_plugin_alconna.uniseg import At
from nonebot_plugin_uninfo import Member
from sqlalchemy import select

from flandre import commandMatcher, Finish
from flandre.annotated import UniMsg, Uninfo, Members
from flandre.message import reply
from flandre.rule import scope

from util.rule import norRule

from .orm import Admin
from .permissionCheck import checkAdmin

rule = norRule & scope('QQClient')

@commandMatcher('op', rule=rule, desc='添加管理员')
async def adminAddMain(members: Members, msgs: UniMsg, info: Uninfo):
	# 处理添加管理员的逻辑
	re = ''
	session = get_session()

	yield checkAdmin(info)

	uids = getAtMembers(msgs, members)

	if len(uids) == 0:
		yield Finish(reply(), '未找到被@的成员，请查看`mc帮助`')
	
	newOp = []
	alreadyOp = []

	async with session.begin():
		for uid in uids.keys():
			if await session.get(Admin, uid):
				alreadyOp.append(uid)
			else:
				session.add(Admin(qq=uid))
				newOp.append(uid)

	if len(newOp) == 0:
		yield Finish(reply(), '以上用户已经全都是OP')

	logger.info(f'新OP:{newOp}，操作者:{info.user.id}')

	re += '将以下用户设置为OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in newOp])
	if alreadyOp:
		re += '\n以下用户已经是OP了:\n' + '\n'.join([f'{uids[i]}({i})' for i in alreadyOp])

	yield reply(), re


@commandMatcher('deop', rule=rule, desc='移除管理员')
async def adminRemoveMain(members: Members,msgs: UniMsg, info: Uninfo):
	# 处理移除管理员的逻辑
	re = ''
	session = get_session()

	yield checkAdmin(info)

	uids = getAtMembers(msgs, members)

	if len(uids) == 0:
		yield Finish(reply(), '未找到被@的成员，请查看`mc帮助`')
	
	rmOp = []
	noOp = []

	async with session.begin():
		for uid in uids.keys():
			if admin := await session.get(Admin, uid):
				await session.delete(admin)
				rmOp.append(uid)
			else:
				noOp.append(uid)

	if len(rmOp) == 0:
		yield Finish(reply(), '以上用户都不是OP，无法移除')

	logger.info(f'移除OP:{rmOp}，操作者:{info.user.id}')

	re += '以下用户不再是OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in rmOp])
	if noOp:
		re += '\n以下用户原本就不是OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in noOp])

	yield reply(), re


@commandMatcher('lsop', rule=rule, desc='查看管理员')
async def adminListMain(members: Members, session: async_scoped_session):
	# 查看当前群组的管理员列表
	usersDict: dict[str, str] = {}
	for member in members:
		usersDict[member.id] = getName(member)
	uids = (await session.scalars(select(Admin))).all()
	ops = []
	for i in uids:
		logger.info(f'{usersDict.get(i.qq,"不在群内")}({i.qq})')
		ops.append(f'{usersDict.get(i.qq,"不在群内")}({i.qq})')
	re = '以下用户为OP用户:\n' + '\n'.join(ops)
	yield reply(), re

def getAtMembers(msg: UniMsg, members: Members) -> dict[str, str]:
	out: dict[str, str] = {}
	usersDict: dict[str, str] = {users.id:getName(users) for users in members }
	for m in msg:
		if isinstance(m, At):
			uid = m.target
			if not (name := usersDict.get(uid)):
				raise ValueError(f'无法获取用户 {uid} 的名称，请检查是否在群内')
			out[uid] = name
		
	return out

def getName(member: Member) -> str:
	if member.nick:
		return member.nick
	elif member.user.name:
		return member.user.name
	else:
		return '获取名称失败'