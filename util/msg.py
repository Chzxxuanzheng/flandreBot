from nonebot.adapters.onebot.v11 import Bot, MessageEvent, PrivateMessageEvent, MessageSegment, Message
from nonebot.log import logger
from .button import Button


def getId(event: MessageEvent)-> int:
	if isinstance(event,PrivateMessageEvent):
		return event.user_id
	else:
		return event.group_id


async def toOffical(bot: Bot, msg: Message|MessageSegment, send = True)->MessageSegment|str:
	if isinstance(msg,MessageSegment):
		msg = Message(msg)
	msg = [MessageSegment.node_custom(('2495495495', 'Flandre Scarlet', msg))]
	id = await bot.call_api('send_forward_msg', messages=msg)
	logger.info(id)
	if send:
		return MessageSegment('longmsg', {'id': id})
	else:
		return id

def createMd(md: str)->MessageSegment:
	md = md.replace('\r\n','\n')
	md = md.replace('\n','\\n')
	md = md.replace('"','\\"')
	md = md.replace('\t','\\t')
	data = {
		"content": '{"content":"' + md + '"}'
	}
	return MessageSegment('markdown', data)


def createButton(buttons: list|Button):
	if isinstance(buttons, Button):
		buttons = [[buttons]]
	else:
		if len(buttons) == 0:
			return
		if not isinstance(buttons[0], list):
			buttons: list[list[Button]] = [buttons]
	rows = []
	for line in buttons:
		elements = []
		for button in line:
			elements.append(button.toData())
		rows.append({'buttons':elements})
	data = {
			'content': {
				'rows': rows
			}
		}
	return MessageSegment('keyboard', data=data)



def createSelfForward(bot: Bot, msgs: list[Message|str]):
	content = Message()
	for msg in msgs:
		content += MessageSegment.node_custom(bot.self_id, 'Flandre Scarlet', msg)
	return content