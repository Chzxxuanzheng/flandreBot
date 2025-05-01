from core.matcher import commandMatcher, finish
from util.rule import norRule, fromUserPrivate
from nonebot_plugin_orm import async_scoped_session
from nonebot .adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from sqlalchemy import select

from .orm import OtpKey
from .config import config

@commandMatcher('2fa', rule=norRule& fromUserPrivate(config.userId), desc='查看已有2fa')
async def tfa(session: async_scoped_session):
	data = (await session.scalars(select(OtpKey))).all()
	re = [f'{i.name}:{i.otp.now()}' for i in data]
	if len(re) == 0:
		finish('未设置2fa。请通过`添加2fa 名称 KEY`添加2fa。')
	yield('\n'.join(re))

@commandMatcher('添加2fa', rule=norRule & fromUserPrivate(config.userId), desc='添加2fa')
async def addTfa(session: async_scoped_session, arg: Message=CommandArg()):
	args = arg.extract_plain_text()
	if not args:
		finish('缺少参数。参数格式为`名称 KEY`')

	args = args.split(' ')
	if len(args) != 2:
		finish('参数格式错误。参数格式为`名称 KEY`')	

	name, key = args
	if not name or not key:
		finish('参数格式错误。参数格式为`名称 KEY`')

	async with session.begin():
		if await session.get(OtpKey, name):
			finish(f'{name}已存在。请通过`更新2fa {name} KEY`更新2fa。')
		session.add(OtpKey(name=name, key=key))
		await session.commit()
	
	yield f'添加{name}到2fa成功。'

@commandMatcher('删除2fa', rule=norRule & fromUserPrivate(config.userId), desc='删除2fa')
async def delTfa(session: async_scoped_session, arg: Message=CommandArg()):
	name = arg.extract_plain_text()
	if not name:
		finish('缺少参数。参数格式为`名称`')
	async with session.begin():
		tfa = await session.get(OtpKey, name)
		if not tfa:
			finish(f'未找到{name}。请通过`2fa`查看已有2fa。')
		await session.delete(tfa)
		await session.commit()
	yield f'删除{name}成功。'

@commandMatcher('更新2fa', rule=norRule & fromUserPrivate(config.userId), desc='更新2fa')
async def updateTfa(session: async_scoped_session, arg: Message=CommandArg()):
	args = arg.extract_plain_text()
	if not args:
		finish('缺少参数。参数格式为`名称 KEY`')

	args = args.split(' ')
	if len(args) != 2:
		finish('参数格式错误。参数格式为`名称 KEY`')	

	name, key = args
	if not name or not key:
		finish('参数格式错误。参数格式为`名称 KEY`')

	async with session.begin():
		tfa = await session.get(OtpKey, name)
		if not tfa:
			finish(f'未找到{name}。请通过`2fa`查看已有2fa。')
		tfa.key = key
		await session.commit()
	
	yield f'更新{name}成功。'

@commandMatcher('验证2fa', rule=norRule & fromUserPrivate(config.userId), desc='验证2fa')
async def verifyTfa(session: async_scoped_session, arg: Message=CommandArg()):
	args = arg.extract_plain_text()
	if not args:
		finish('缺少参数。参数格式为`名称 TOTP`')

	args = args.split(' ')
	if len(args) != 2:
		finish('参数格式错误。参数格式为`名称 TOTP`')	

	name, totp = args
	if not name or not totp:
		finish('参数格式错误。参数格式为`名称 TOTP`')

	async with session.begin():
		tfa = await session.get(OtpKey, name)
		if not tfa:
			finish(f'未找到{name}。请通过`2fa`查看已有2fa。')
		if not tfa.otp.verify(totp):
			finish(f'TOTP 验证失败。')
		yield f'验证{name}成功。'