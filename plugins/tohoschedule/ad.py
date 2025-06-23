from asyncio import sleep
from nonebot import require, get_bots
from nonebot.adapters.milky import MessageSegment, Bot, Message
from random import randint as rand

from .config import Config
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

async def main():
	bot: Bot = get_bots()['2490693685']
	groupList = [i['group_id'] for i in await bot.call_api('get_group_list')]
	for i in groupList:
		msg: list[Message] = []
		msg.append(MessageSegment.text("ad:"))
		msg.append(MessageSegment.text("第二十回东方人气投票将于8月9日至8月23日执行，大家别忘了到官方网站https://toho-vote.info上为“フランドール スカーレット”投票。"))
		await bot.send_msg(message_type="group",group_id=i,message=msg)

scheduler.add_job(main, trigger='cron', hour=10, minute=0, id='ad')