from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot import logger
from util.api import getForwardMsg, getGroupMemberName
from util.rule import fromGroup
from .rcon import rcon
from json import dumps
from .config import config

# 要转发的群
GROUP_INFO: dict[int, str] = config.forward.groups

match = on_message(rule=fromGroup(GROUP_INFO.keys()), priority=0, block=False)

@match.handle()
async def main(event: GroupMessageEvent):
	gid = event.group_id
	uid = event.user_id
	msg = event.message
	if not gid in GROUP_INFO:
		return
	logger.info(f'转发消息 群:{gid} 用户:{uid} 内容:{msg.extract_plain_text()}')
	send = await createRe(event)
	rcon(f'tellraw @a {dumps(send, ensure_ascii=False)}')

def mcMsg(content: str, color: str='white'):
	# 过滤不可见字符
	text = ''
	for char in content:
		if char.isprintable() or char=='\n':text += char
	return {'text':text,'color':color}

def newLine():
	return mcMsg('\n')

async def userName(gid, uid):
	return mcMsg(await getGroupMemberName(gid, uid), 'blue')

async def groupName(gid):
	groupName = GROUP_INFO[gid]
	return mcMsg(groupName, 'green')

async def createHead(gid, uid) -> list[dict[str|str]]:
	return [mcMsg('['),await groupName(gid),mcMsg('-'),await userName(gid, uid),mcMsg(']')]

async def MsgToMcMsg(msg: MessageSegment):
	if msg.type == 'text':
		return mcMsg(msg.data['text'])
	elif msg.type == 'image':
		return mcMsg(msg.data['summary'], 'gray')
	elif msg.type == 'at':
		return mcMsg(msg.data['name'], 'yellow')
	elif msg.is_text():
		return mcMsg(msg.data['text'])
	elif msg.type == 'reply':
		return mcMsg('')
	elif msg.type == 'forward':
		forward = await getForwardMsg(msg.data['id'])
		return mcMsg(f'合并转发({len(forward)})条', 'gray')
	else:
		logger.info(msg.type)
		logger.info(msg.data)
		return mcMsg('不可识别消息', 'gray')

def haveNewLine(msg: list[dict|dict])-> bool:
	for i in msg:
		if i['text'] == '\n':return True
	return False

async def createRe(event: GroupMessageEvent)-> list[dict[str|str]]:
	gid = event.group_id
	uid = event.user_id
	msg = event.message
	head = await createHead(gid, uid)
	body = await createMsg(msg)
	if event.reply:
		reps = event.reply.message
		reps = await createMsg(reps)
		for rep in reps:
			rep['italic'] = True
			rep['underlined'] = True
		body = [*reps, newLine(), *body]

	return [*head, newLine(), *body]

async def createMsg(msgs: Message):
	return [await MsgToMcMsg(msg) for msg in msgs]