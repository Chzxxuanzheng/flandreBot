from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot_plugin_orm import get_session
from core import finish

from .orm import Admin

async def checkAdmin(event:MessageEvent):
	session = get_session()

	async with session.begin():
		if not await session.get(Admin, event.user_id):
			finish([MessageSegment.reply(event.message_id), '无权操作，请确保你是OP'])