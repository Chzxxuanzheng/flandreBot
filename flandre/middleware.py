from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException

from flandre.annotated import Uninfo

@run_preprocessor
async def ignoreSelf(session: Uninfo):
	if session.user.id == session.self_id:
		raise IgnoredException('ignore self message')