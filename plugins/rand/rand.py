from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent
from nonebot.params import CommandArg
from core.matcher import commandMatcher

from random import randint

@commandMatcher('rand', 'rnd', desc='随机数')
async def main(event: MessageEvent, args: Message = CommandArg()):
	args: str = args.extract_plain_text()
	yield Message([MessageSegment.text(process(args)),
							MessageSegment.reply(event.message_id)])

def process(arg: str)->str:
	if arg == "":
		return f'{randint(1,6)}'
	elif arg.isdecimal():
		return f'{randint(1,int(arg))}'
	else:
		arg.replace('，', ',')
		if "," in arg:
			return twoStrToRand(arg, ",")
		else:
			return twoStrToRand(arg, " ")


async def twoStrToRand(args: str, split: str):
	argList = args.split(split)
	if len(argList) != 2:
		return "格式错误"
	else:
		for i in argList:
			if not i.isdecimal():
				return "格式错误"
		return f'{randint(int(argList[0]),int(argList[1]))}'