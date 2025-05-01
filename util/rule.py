from nonebot.params import CommandStart
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, MessageEvent, PrivateMessageEvent
from nonebot import get_driver
from nonebot.rule import Rule, to_me
# 通常规则
async def norRule(event: Event, com: str = CommandStart()) -> bool:
	#@的话无视条件
	if event.is_tome():
		return True
	#至少有一个开始符号
	if com == "":
		return False
	return True

norRule = Rule(norRule)

# 来自规定群组规则
def fromGroup(groups: list[int|str]|int|str):
	if type(groups) == int or type(groups) == str:
		groups = [int(groups)]
	else:
		groups = [int(i) for i in groups]
	async def re(event: GroupMessageEvent) -> bool:
		if event.group_id in groups:
			return True
		return False
	return Rule(re)

# 来自规定用户规则
def fromUser(users: list[int|str]|int|str):
	if type(users) == int or type(users) == str:
		users = [int(users)]
	else:
		users = [int(i) for i in users]
	async def re(event: MessageEvent) -> bool:
		if event.user_id in users:
			return True
		return False
	return Rule(re)

fromSu = fromUser(get_driver().config.superusers)

# 来自规定用户私聊规则
def fromUserPrivate(users: list[int|str]|int|str):
	if type(users) == int or type(users) == str:
		users = [int(users)]
	else:
		users = [int(i) for i in users]
	async def re(event: PrivateMessageEvent) -> bool:
		if event.user_id in users:
			return True
		return False
	return Rule(re)

# #删除起始字符
# def rmStartChar(com: str):
# 	for i in get_driver().config:
# 		i = str(i)
# 		com = com.replace(i, '')
# 	return com