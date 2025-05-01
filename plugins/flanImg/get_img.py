from nonebot import logger
from random import shuffle
from os import listdir
from os.path import join
from nonebot.adapters.onebot.v11 import MessageSegment, Message

#获取随机图片
def getImg(path: str, num: int) -> list[Message]:
	imgList = listdir(path)
	shuffle(imgList)
	outList = []
	logger.info(f"共发送{num}张图片")
	for i in range(num):
		name = imgList[i]
		logger.info(f"图片名:{name}")
		with open(join(path, name), "rb")as f:
			outList.append(Message(MessageSegment.image(f.read())))
	return outList