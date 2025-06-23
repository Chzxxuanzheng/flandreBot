from nonebot.params import CommandStart
from nonebot.adapters import Event
from nonebot import get_driver
from nonebot.rule import Rule, to_me
# 通常规则
async def _norRule(event: Event, com: str = CommandStart()) -> bool:
	#@的话无视条件
	if event.is_tome():
		return True
	#至少有一个开始符号
	if com == "":
		return False
	return True

norRule = Rule(_norRule)