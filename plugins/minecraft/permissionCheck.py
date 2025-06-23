from nonebot_plugin_orm import get_session
from flandre import Finish
from flandre.annotated import Uninfo
from flandre.message import reply

from nonebot_plugin_alconna.uniseg import Text

from .orm import Admin

async def checkAdmin(info: Uninfo):
	session = get_session()

	async with session.begin():
		if not await session.get(Admin, info.user.id):
			yield Finish(
				reply(),
				Text('无权操作，请确保你是OP')
			)