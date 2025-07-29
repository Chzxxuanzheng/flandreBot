from flandre import messageMatcher, Finish
from flandre.annotated import Uninfo
from nonebot.rule import Rule
from nonebot.internal.matcher import current_bot, current_event
from nonebot.adapters.minecraft.event.base import BasePlayerCommandEvent, BaseDeathEvent
from nonebot_plugin_uninfo import SupportScope, get_interface, Interface
from nonebot_plugin_alconna.uniseg import UniMsg, UniMessage, Target, Segment, Text, At, AtAll, Image, Reply

from typing import Iterable

from .config import config

async def _rule(session: Uninfo) -> bool:
	if session.scope not in (SupportScope.minecraft, SupportScope.qq_client):
		return False
	if session.scope == SupportScope.qq_client:
		if session.group is None:
			return False
		if session.group.id not in config.forward.groups:
			return False
	return True

@messageMatcher(desc='Mc/QQ双向转发', rule=Rule(_rule), priority=20, block=False)
async def forward(session: Uninfo, msg: UniMsg):
	if session.scope == SupportScope.minecraft:
		yield mcToQQ(session, msg)
	elif session.scope == SupportScope.qq_client:
		yield qqToMc(session, msg)


async def mcToQQ(session: Uninfo, msg: UniMsg):
	name = session.user.name
	if not name:raise ValueError('User name is required for forwarding messages from Minecraft to QQ.')
	# 过滤指令
	if isinstance(current_event.get(), BasePlayerCommandEvent): return
	if isinstance(current_event.get(), BaseDeathEvent):
		yield Finish(joke(name, str(msg)))
	msg = UniMessage(f'[{name}] ') + msg
	for group in config.forward.groups.keys():
		yield Target.group(str(group), SupportScope.qq_client)
		yield msg


async def qqToMc(session: Uninfo, msg: UniMsg):
	bot = current_bot.get()
	interface = get_interface(bot)
	if not interface:
		raise ValueError('Interface is required for forwarding messages from QQ to Minecraft.')
	head = craeteHead(session)
	mainMsg = await toMcMsg(msg, session, interface)

	yield Target.group('0', SupportScope.minecraft)
	yield head + '\n' + UniMessage(mainMsg)

def craeteHead(session: Uninfo) -> UniMsg:
	re = UniMessage()
	re += Text('[')
	re += mcMsg(config.forward.groups[session.group.id]).color('green') # type: ignore
	re += Text('|')
	re += mcMsg(session.member.nick if session.member.nick else session.member.user.name).color('blue') # type: ignore
	re += Text(']')
	return re

async def toMcMsg(msgs: Iterable[Segment], session: Uninfo, interface: Interface) -> Iterable[Text]:
	re = []
	for msg in msgs:
		if isinstance(msg, Text):
			re.append(msg)
		elif isinstance(msg, At):
			user = await interface.get_member(
				session.scene.type,
				session.group.id, # type: ignore
				msg.target
			)
			if not user:
				re.append(mcMsg(f'@昵称获取失败({msg.target})').color('yellow'))
			elif user.nick:
				re.append(mcMsg(f'@{user.nick}').color('yellow'))
			elif user.user.nick:
				re.append(mcMsg(f'@{user.user.nick}').color('yellow'))
			else:
				re.append(mcMsg(f'@{user.user.name}').color('yellow'))
		elif isinstance(msg, AtAll):
			re.append(mcMsg('@全体成员').color('yellow'))
		elif isinstance(msg, Image):
			re.append(mcMsg(f'[图片]').color('gray'))
		elif isinstance(msg, Reply):
			re.extend(await createReply(msg, session, interface))
		else:
			re.append(mcMsg(f'[未知消息]').color('gray'))
	return re

async def createReply(reply: Reply, session: Uninfo, interface: Interface) -> Iterable[Text]:
	txt = await getReplyMsg(reply, session, interface)
	paintext = ''.join(i.text for i in txt)
	length = [ulen(i) for i in paintext.split('\n')]
	length = max(length) if length else 0
	if length < 10: length = 10
	elif length > 80: length = 80
	frontLength = (length - 4) // 2
	backLength = length - 4 - frontLength
	head = Text('━' * frontLength + '引用' + '━' * backLength + '\n').color('gray')
	foot = Text('\n' + '━' * length + '\n').color('gray')
	return [head, *txt, foot]

async def getReplyMsg(reply: Reply, session: Uninfo, interface: Interface) -> Iterable[Text]:
	if not reply.msg:return [Text('识别失败').color('gray')]
	if isinstance(reply.msg, str): return [Text(reply.msg)]
	return await toMcMsg(UniMessage.generate_sync(
				message=reply.msg,
				bot=current_bot.get(),
				event=current_event.get(),
			), session, interface)
		# elif isinstance(msg, Voice):
		# 	return UniMessage(f'语音({msg.data["summary"]})')
		# elif isinstance(msg, Video):
		# 	return UniMessage(f'视频({msg.data["summary"]})')
		# elif isinstance(msg, File):
		# 	return UniMessage(f'文件({msg.data["summary"]})')
		# elif isinstance(msg, Reply):
		# 	return UniMessage('回复消息')
		# else:
		# 	return UniMessage('未知消息类型')

# async def MsgToMcMsg(msg: UniMsg) -> UniMsg:
# 	if msg.type == 'text':
# 		return mcMsg(msg.data['text'])
# 	elif msg.type == 'image':
# 		return mcMsg(msg.data['summary'], 'gray')
# 	elif msg.type == 'at':
# 		return mcMsg(msg.data['name'], 'yellow')
# 	elif msg.is_text():
# 		return mcMsg(msg.data['text'])
# 	elif msg.type == 'reply':
# 		return mcMsg('')
# 	elif msg.type == 'forward':
# 		forward = await getForwardMsg(msg.data['id'])
# 		return mcMsg(f'合并转发({len(forward)})条', 'gray')
# 	else:
# 		logger.info(msg.type)
# 		logger.info(msg.data)
# 		return mcMsg('不可识别消息', 'gray')

def mcMsg(content: str)-> Text:
	# 过滤不可见字符
	text = ''
	for char in content:
		if char.isprintable() or char=='\n':text += char
	return Text(content)

# 嘲笑某人
def joke(name: str, content: str) -> str:
	from random import choice
	list = [
        '很不幸,{content}',
        '今天是{name}的幸运日,{content}',
        '{name}又出事了,{content}',
        '今天是一个好日子,所以{content}',
        '不出所料,{content}',
        '果然,{content}',
        '毫无意外,{content}',
        '正如大家所料,{content}',
        '看起来,{content}',
        '显然,{content}',
        '终于,{content}',
        '哎呀,{content}',
        '噢不,{content}',
        '我就知道,{content}',
        '不意外,{content}',
        '啊这,{content}',
        'emmm,{content}',
        '好家伙,{content}',
        '真巧,{content}',
        '刚刚,{content}',
        '突然,{content}',
        '瞬间,{content}',
        '一不小心,{content}',
        '看样子,{content}',
        '据说,{content}',
        '传言,{content}',
        '听说,{content}',
        '有消息称,{content}',
        '让我们为{name}默哀0秒,{content}',
    ]
	return choice(list).format(name=name, content=content)
	

import unicodedata

def ulen(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(char) in 'FWA' else 1 for char in s)