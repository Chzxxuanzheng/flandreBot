from typing import Any, AsyncGenerator, Callable, Iterable, Literal
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from inspect import isasyncgenfunction
from core.event import EmitEvent
from core.target import TargetType

type MsgS = str|MessageSegment
type Msg = str|Message|MessageSegment|list[MsgS]
type Handler = Callable[[Any], AsyncGenerator[None|Msg,None]]
type Sender = Callable[[Handler, Any], int]

class FinishMatcherProcess(Exception):
	# 自定义异常类，用于提前结束Matcher处理过程
	def __init__(self, msg, *args):
		super().__init__(*args)
		self.msg = msg

class RecallMsg:
	def __init__(self, id: int):
		'''
		:param id: 要撤回的消息的id，该ID为在**事件响应函数**中发送的消息顺序，**而非**message_id
		'''
		self.id = id

def finish(msg: Any)-> None:
	# 抛出自定义异常，用于提前结束Matcher处理过程
	raise FinishMatcherProcess(msg)

async def _matcherIter(func, *args, **kwargs)-> AsyncGenerator[Any,None]:
	# 异步迭代处理函数返回的消息，处理自定义异常
	try:
		if isasyncgenfunction(func):
			async for msg in func(*args, **kwargs):
				if not msg:continue
				yield msg
		else:
			msg = await func(*args, **kwargs)
			if not msg:return
			yield msg
	except FinishMatcherProcess as e:
		yield e.msg
		return
	
def createSender(bot: Bot, event: Event)-> Sender:
	# 根据事件类型创建对应的Sender
	if isinstance(event, EmitEvent):
		return createEmiEventSender(bot, event)
	elif isinstance(event, Event):
		return createNorEventSender(bot, event)
	else:
		raise ValueError('event类型错误')

def createEmiEventSender(bot: Bot, event: EmitEvent)-> Sender:
	# 创建用于EmitEvent的Sender
	target = event.target
	if target.type == TargetType.PRIVATE:
		return createBaseSender(bot, target.id, 'private')
	else:
		return createBaseSender(bot, target.id, 'group')

def createNorEventSender(bot: Bot, event: Event)-> Sender:
	# 创建用于普通Event的Sender
	if isinstance(event, PrivateMessageEvent):
		return createBaseSender(bot, event.user_id, 'private')
	else:
		return createBaseSender(bot, event.group_id, 'group')


def createBaseSender(bot: Bot, targetId: int|str|Iterable[int|str], type: Literal['group', 'private'])-> Sender:
	if type == 'group':
		sendNor = sendGroupNormalMsg
		sendFor = sendGroupForwardMsg
	else:
		sendNor = sendPrivateNormalMsg
		sendFor = sendPrivateForwardMsg

	async def send(msg) -> int:
		return await sendMsg(sendNor, sendFor, bot, targetId, msg)

	async def sender(handler: Handler, *args, **kwargs)-> None:
		msgCache = []
		async for msg in _matcherIter(handler, *args, **kwargs):
			if isinstance(msg, RecallMsg):
				if msg.id >= len(msgCache):
					raise ValueError(f'撤回的消息序号({msg.id})超出消息缓存范围({len(msgCache)})')
				await bot.delete_msg(message_id=msgCache[msg.id])
			else:
				msgCache.append(await send(msg))
	
	return sender


async def sendMsg(
		sendNorMsg: Callable[[Bot, int, Msg], int],
		sendForMsg: Callable[[Bot, int, Msg], int],
		bot: Bot,
		targetId: int|str|Iterable[int|str],
		msg: Msg)-> int:
	# 发送消息，根据消息类型选择不同的发送方法
	hasNode = False
	hasOther = False
	if type(msg) == str:
		msg = Message(msg)
	else:
		if isinstance(msg, MessageSegment):
			msg = Message(msg)
		re = []
		for seg in msg:
			if type(seg) == str:
				seg = MessageSegment.text(seg)
			if seg.type == 'node':
				if hasOther:
					raise ValueError('Message不能同时包含`node`和其他类型的MessageSegment')
				hasNode = True
			else:
				if hasNode:
					raise ValueError('Message不能同时包含`node`和其他类型的MessageSegment')
				hasOther = True
			re.append(seg)
		msg = Message(re)

	if type(targetId) == int or type(targetId) == str:
		targetId = [targetId]
	for id in targetId:
		if hasNode:
			return await sendForMsg(bot, id, msg)
		else:
			return await sendNorMsg(bot, id, msg)

async def sendGroupNormalMsg(bot: Bot, groupId: int, msg: Message)-> int:
	# 发送群聊普通消息
	return (await bot.send_group_msg(group_id=str(groupId), message=msg))['message_id']

async def sendGroupForwardMsg(bot: Bot, groupId: int, msg: Message)-> int:
	# 发送群聊合并转发消息
	return (await bot.send_group_forward_msg(group_id=int(groupId), messages=msg))['message_id']

async def sendPrivateNormalMsg(bot: Bot, userId: int, msg: Message)-> int:
	# 发送私聊普通消息
	return (await bot.send_private_msg(user_id=str(userId), message=msg))['message_id']

async def sendPrivateForwardMsg(bot: Bot, userId: int, msg: Message)-> int:
	# 发送私聊合并转发消息
	return (await bot.send_private_forward_msg(user_id=str(userId), messages=msg))['message_id']