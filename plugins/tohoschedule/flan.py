from asyncio import sleep
from nonebot import require, get_bots
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Message
from random import randint as rand

from .config import Config
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

async def main():
	bot: Bot = get_bots()['2490693685']
	msg: list[Message] = []
	msg.append(MessageSegment.text('@全体成员'))
	msg.append(MessageSegment.text(" "))
	msg.append(MessageSegment.at('2431149266'))
	msg.append(MessageSegment.text("敢日二小姐！\n"))
	msg.append(MessageSegment.text("——来自群管理员（2665924795）的编辑"))
	await bot.send_msg(message_type="group",group_id="871835811",message=msg)

scheduler.add_job(main, trigger='cron', hour=16, minute=1, id='flan')

# async def morning():
# 	bot: Bot = get_bots()['2490693685']
# 	msg = []
# 	if rand(4) == 0:
# 		msg.append('哈~为啥睡觉时间会有一只蠢鸡在这里叫叫叫……')
# 	elif rand(3) == 0:
# 		msg.append('唔~吵死了,这是从那里来的野鸡')
# 		msg.append('「QED」四百九十五年的波纹')
# 	elif rand(2) == 0:
# 		msg.append('大白天的叫什么叫?还让不让芙兰睡觉了?')
# 		msg.append('等会含咲夜过来给你宰了煲鸡汤')
# 	else:
# 		msg.append('那里来的傻鸡?芙兰刚闭眼就叫叫叫')
# 	for i in msg:
# 		await sleep(5 + rand(5))
# 		await bot.send_msg(message_type="group",group_id="871650455",message=MessageSegment.text(i))

# scheduler.add_job(morning, trigger='cron', hour=8, minute=0, id='flanM')
