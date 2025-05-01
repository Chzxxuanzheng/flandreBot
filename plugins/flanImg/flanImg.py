from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent, Bot
from nonebot.params import CommandArg
from nonebot import logger

from .get_img import *
from .config import config

from util.msg import createSelfForward
from util.rule import norRule
from core.matcher import commandMatcher, finish

@commandMatcher(*config.norCmd, rule=norRule, desc='发芙兰图')
async def norImg(bot: Bot, args: Message = CommandArg()):
	# 图片路径
	path = config.norPath
	# 创建图片Message列表
	imgList = await getImgList(path, getNum(args))

	async for i in sendImg(bot, imgList):yield i

@commandMatcher(*config.sexCmd, rule=norRule, desc='发芙兰色图')
async def sexImg(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
	# 图片路径
	path = config.sexPath
	# 创建图片Message列表
	imgList = await getImgList(path, getNum(args))

	async for i in sendImg(bot, imgList):yield i

async def sendImg(bot: Bot, imgs: list[Message]):
	logger.debug(imgs)
	if len(imgs) <= config.maxSendNum:
		for i in imgs:
			yield i
	else:
		msg = createSelfForward(bot, imgs)
		yield msg
		# await bot.call_api("send_private_forward_msg",user_id=2431149266,messages=msg)
		# await bot.send_private_forward_msg(user_id=2431149266, message=msg)

#求发几张
def getNum(args):
	num = args.extract_plain_text()
	if num.isdecimal():
		num = int(num)
		if num <= 0:
			num = 1
	else:
		num = 1
	return num

#制作图片列表
async def getImgList(path, num) -> list[Message]|None:
	try:
		return getImg(path, num)
	except Exception as ex:
		logger.error(ex)
		finish([MessageSegment.at(2431149266), "读取图库失败"])