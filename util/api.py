from nonebot.adapters.onebot.v11 import Bot
from nonebot import get_driver as __get_driver

__bot: Bot = None

def setBot(bot: Bot):
	global __bot
	__bot = bot

__get_driver().on_bot_connect(setBot)

async def getGroupMemberName(gid: int, uid: int):
	userInfo = await __bot.call_api('get_group_member_info',group_id=gid,user_id=uid)
	if userInfo['card']:
		return userInfo['card']
	else:
		return userInfo['nickname']
	
async def getForwardMsg(id: str)->list[dict[str|str]]:
	re = await __bot.call_api('get_forward_msg', id=id)
	return re['message']

async def getGroupMemberList(gid)->list[dict[str|str]]:
	return await __bot.call_api('get_group_member_list', group_id=gid)