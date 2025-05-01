from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Message
from nonebot.params import CommandArg
from nonebot_plugin_orm import async_scoped_session
from nonebot.log import logger
from asyncio import sleep
from sqlalchemy import select

from core import commandMatcher, finish

from .rcon import rcon
from .orm import Player
from .permissionCheck import checkAdmin

@commandMatcher('auth', '认证', desc='认证登陆MC')
async def authMain(event: MessageEvent, session: async_scoped_session):
	ids = (await session.scalars(select(Player).where(Player.qq == event.user_id))).all()

	if len(ids) == 0:
		finish([MessageSegment.reply(event.message_id), '你还没有绑定的MC账户，请先绑定MC账户。具体操作为">认证绑定 MC账户ID"'])

	for i in range(60):
		if id := await tryAuth([i.id for i in ids]):
			logger.info(f'已批准{id}的登陆')
			finish([MessageSegment.reply(event.message_id), f'已批准{id}的登陆'])
		await sleep(1)
	
	finish([MessageSegment.reply(event.message_id), f'超时，在1分钟内，您没有任何账户登陆'])

@commandMatcher('认证绑定', desc='绑定MC账户')
async def authAddMain(event: MessageEvent, session: async_scoped_session, args: Message =  CommandArg()):
	args = args.extract_plain_text()
	if not args: finish([MessageSegment.reply(event.message_id), f'用法不对，请输入需要的绑定的账户ID，如">认证绑定 Mr.Lee"(将Mr.Lee换成你的MC账户ID)'])
	
	if player := await session.get(Player, args):
		finish([MessageSegment.reply(event.message_id), f'{args}已经被{player.qq}绑定'])
	
	player = Player(id=args, qq=event.user_id)
	session.add(player)

	logger.info(f'新绑定{args}->{player.qq}')

	await session.commit()
	finish([MessageSegment.reply(event.message_id), f'绑定{args}成功'])


@commandMatcher('认证列表', desc='查看已绑定MC账户')
async def authListMain(event: MessageEvent, session: async_scoped_session):
	players = (await session.scalars(select(Player))).all()
	if not len(players): finish([MessageSegment.reply(event.message_id), f'暂时没有绑定数据'])
	qqMap: dict[str|list[str]] = {}
	for player in players:
		if player.qq in qqMap:
			qqMap[player.qq].append(player.id)
		else:
			qqMap[player.qq] = [player.id]

	msgs = []
	for i in qqMap.keys():
		msg = f'{i}:\n > '
		msg += '\n > '.join(qqMap[i])
		msgs.append(msg)

	finish([MessageSegment.reply(event.message_id), '\n'.join(msgs)])


@commandMatcher('我的认证列表', desc='查看自己绑定的MC账户')
async def authMyListMain(event: MessageEvent, session: async_scoped_session):
	players = (await session.scalars(select(Player).where(Player.qq == event.user_id))).all()
	if not len(players): finish([MessageSegment.reply(event.message_id), f'暂时没有绑定数据'])

	ids = [f'> {i.id}' for i in players]
	logger.info(ids)
	msg = '\n'.join(ids)

	finish([MessageSegment.reply(event.message_id), msg])


@commandMatcher('认证解绑', desc='解绑MC账户')
async def authRemoveMain(event: MessageEvent, session: async_scoped_session, id: Message = CommandArg()):
	id = id.extract_plain_text()
	if player := await session.get(Player, id):
		if player.qq != str(event.user_id):
			finish([MessageSegment.reply(event.message_id), f'{id}属于{player.qq},你无权操作'])
		re = f'解绑{id}成功'
		await session.delete(player)
		await session.commit()
		logger.info(f'{event.user_id}{re}')
		finish([MessageSegment.reply(event.message_id), re])
	finish([MessageSegment.reply(event.message_id), f'未能在你绑定的MC账户ID范围内找到{id}，请通过">我的认证列表"来确认{id}是否已经和你绑定'])


@commandMatcher('认证强制解绑', desc='强制解绑MC账户')
async def authForceRemoveMain(event: MessageEvent, session: async_scoped_session, id: Message = CommandArg()):
	await checkAdmin(event)

	id = id.extract_plain_text()

	if not id:
		finish([MessageSegment.reply(event.message_id), f'用法不对。正确用法:">认证强制解绑 MC账户ID"'])

	if player := await session.get(Player, id):
		re = f'成功将{player.id}从{player.qq}上面解绑'
		await session.delete(player)
		await session.commit()
		logger.info(f'{event.user_id}{re}')
		finish([MessageSegment.reply(event.message_id), re])
	
	finish([MessageSegment.reply(event.message_id), f'未找到名为{id}的MC账户'])
			

async def tryAuth(ids: list[str])->str|None:
	for id in ids:
		re = rcon(f'authme forcelogin {id}')
		if re == f'Force login for {id} performed!':
			return id
	return None
