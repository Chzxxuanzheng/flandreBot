from typing import Iterable
from nonebot.adapters import Bot
from nonebot.internal.matcher import current_bot
from nonebot_plugin_alconna.uniseg import Segment, Text, UniMessage, Reply, get_message_id, Reference, CustomNode

type seg = Segment|str|int
type Msg = UniMessage|Iterable[seg]|seg

def toUniMsg(*msg: Msg) -> UniMessage:
	"""将消息转换为 UniMsg"""
	if len(msg) == 0:
		return UniMessage()
	elif len(msg) == 1:
		m = msg[0]
		if isinstance(m, UniMessage):
			return m
		elif isinstance(m, str):
			return UniMessage(Text(m))
		elif isinstance(m, Iterable):
			return toUniMsg(*m)
		else:
			return UniMessage(toUniSeg(m))
	else:
		re = UniMessage()
		for m in msg:
			if isinstance(m, UniMessage):
				re += m
			elif isinstance(m, str):
				re += Text(m)
			elif isinstance(m, Iterable):
				re += toUniMsg(*m)
			else:
				re += toUniSeg(m)
			
		return re

def toUniSeg(msg: seg) -> Segment:
	"""将消息转换为 UniSeg"""
	if isinstance(msg, Segment):
		return msg
	else:
		return Text(str(msg))
	
def toPlaintext(msg: UniMessage) -> str:
	re = ''
	for m in msg:
		if isinstance(m, Text):
			re += m.text

	return re

def reply() -> Reply:
	"""返回一个当前消息的回复消息"""
	return Reply(get_message_id())

def selfForward(*msg: Msg, bot: Bot|None = None) -> UniMessage:
	"""返回一个自身合并转发消息"""
	if bot is None:
		bot = current_bot.get()
	forward = []
	for m in msg:
		node = CustomNode(
			uid=bot.self_id,
			name='合并转发',
			content=toUniMsg(m),
		)
		forward.append(node)
	return UniMessage(
		Reference(
			nodes=forward,
		)
	)