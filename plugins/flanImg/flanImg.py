from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot import logger
from nonebot_plugin_alconna.uniseg import Image

from os import listdir
from os.path import join
from random import shuffle

from .config import config

from util.rule import norRule
from flandre.matcher import commandMatcher
from flandre.rule import scope
from flandre.message import selfForward

rule = norRule & scope('QQClient')

@commandMatcher(*config.norCmd, rule=rule, desc='发芙兰图')
async def norImg(args: Message = CommandArg()):
	# 图片路径
	path = config.norPath
	yield main(path, getNum(args))

@commandMatcher(*config.sexCmd, rule=rule, desc='发芙兰色图')
async def sexImg(args: Message = CommandArg()):
	# 图片路径
	path = config.sexPath
	yield main(path, getNum(args))


async def main(path: str, num: int):
	"""主函数，获取图片列表"""
	try:
		imgs = getImg(path, num)
		if len(imgs) <= config.maxSendNum:
			for i in imgs:
				yield i
		else:
			yield selfForward(*imgs)
	except:
		yield '发生图片失败'
		raise

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


#获取随机图片
def getImg(path: str, num: int) -> list[Message]:
	imgList = listdir(path)
	shuffle(imgList)
	outList = []
	logger.info(f"共发送{num}张图片")
	for i in range(num):
		name = imgList[i]
		logger.info(f"图片名:{name}")
		outList.append(Image(path=join(path, name)))
	return outList