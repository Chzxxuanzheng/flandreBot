from flandre.matcher import commandMatcher
from util.rule import norRule

from nonebot.params import CommandArg
from nonebot.adapters import Message

async def noArgs(msg: Message = CommandArg())-> bool:
	if len(msg) == 0:
		return True
	return False

@commandMatcher('ping', 'p', desc='ping', rule=norRule & noArgs)
async def ping():
	yield 'pong'