from nonebot.adapters.onebot.v11 import MessageSegment
from pillowmd import MdStyle
from io import BytesIO

async def md2pic(md: str, style: MdStyle) -> MessageSegment:
	buf = BytesIO()
	(await style.AioRender(md)).image.save(buf, format='PNG')
	return MessageSegment.image(buf)