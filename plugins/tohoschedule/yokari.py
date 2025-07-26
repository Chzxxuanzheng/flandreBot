from nonebot_plugin_alconna.uniseg import Text, Image
from flandre import cronMatcher
from pathlib import Path

# @cronMatcher(msgType='group', id='871835811', hour=17, minute=8, desc='非遗1')
@cronMatcher(msgType='group', id='871835811', hour='16', minute='0', desc='非遗1')
async def main():
	yield [
		Text('@全体成员'),
		Text(" 我们群主敢日八云紫！\n"),
		Image(path=Path(__file__).parent / 'yokari.png'),
		Text("——来自群管理员（2665924795）的编辑"),
	]
