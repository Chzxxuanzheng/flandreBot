from .config import config
from nonebot import logger

from flandre import commandMatcher
from flandre.annotated import plaintextArg
from nonebot_plugin_anan_say.render import render
from pathlib import Path
from io import BytesIO

from nonebot_plugin_alconna.uniseg import Image

@commandMatcher('安安说', desc='安安说')
async def anan_say(txt: str = plaintextArg()):
	if not txt:
		txt = '你想让吾辈说些什么呢？'

	img = draw(txt)
	if not img:
		img = draw('吾辈写不了这么多字呢')
		if not img:
			yield '渲染失败！请调整最小字号'
			return
	
	buf = BytesIO()
	img.save(buf, format='PNG')
	yield Image(raw=buf.getvalue())
		
def draw(data: str):
	return render(
		data,
		200,
		40,
		str(Path(__file__).parent / 'SourceHanSansCN_Regular.otf'),
	)