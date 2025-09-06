from nonebot import logger
from flandre import commandMatcher
from flandre.annotated import arg, UniMessage
from pathlib import Path
import pillowmd
from nonebot_plugin_alconna.uniseg import Text, At, Image, AtAll
from nonebot_plugin_uninfo import QryItrface, Uninfo
from nonebot_plugin_exdi import di
from uuid import uuid4
from typing import IO, Literal
import tempfile

from .process import process

style = pillowmd.LoadMarkdownStyles(Path(__file__).parent / 'style')

cacheData: dict[str, list[IO[bytes]]] = {}

@commandMatcher('拍屏', desc='生成拍屏效果图')
async def screen_shot(msgs: UniMessage = arg()):
	id = str(uuid4())
	cacheData[id] = []
	txt = await toMd(msgs = msgs, id = id) # type: ignore
	img = newImg(id)
	(await style.AioRender(txt, useImageUrl=True)).image.save(img.name)
	logger.success(f'生成md图片: {img.name}')
	process(img.name)
	yield Image(path=img.name)
	for f in cacheData[id]:
		f.close()


@di()
async def toMd(interface: QryItrface, session: Uninfo, msgs: UniMessage, id: str) -> str:
	data: list[tuple[Literal['txt', 'img'], str]] = []
	for msg in msgs:
		if isinstance(msg, Text):
			data.append(('txt', msg.text))
		elif isinstance(msg, At):
			user = await interface.get_member(
				session.scene.type,
				session.group.id, # type: ignore
				msg.target
			)
			if not user:
				data.append(('txt', f'@昵称获取失败({msg.target})'))
			elif user.nick:
				data.append(('txt', f'@{user.nick}'))
			elif user.user.nick:
				data.append(('txt', f'@{user.user.nick}'))
			else:
				data.append(('txt', f'@{user.user.name}'))
		elif isinstance(msg, AtAll):
			data.append(('txt', f'@全体成员'))
		elif isinstance(msg, Image):
			data.append(('img', f'![图片]({msg.url})'))
		else:
			data.append(('txt', f'[未知消息]'))
	re = ''
	lastType: Literal['txt', 'img'] = 'txt'
	for t, v in data:
		if t == 'txt':
			if lastType == 'img':
				re += '\n'
			re += v
			lastType = 'txt'
		else:
			if lastType == 'txt' and not re.endswith('\n'):
				re += '\n'
			re += v
			lastType = 'img'
	return re

def newImg(id: str) -> IO[bytes]:
	img = tempfile.NamedTemporaryFile(mode='w+b', suffix='.png', delete=False)
	cacheData[id].append(img)
	return img