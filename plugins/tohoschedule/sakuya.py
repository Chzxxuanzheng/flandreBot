from flandre import cronMatcher
from pathlib import Path
from nonebot_plugin_alconna.uniseg import Text, Image

# @cronMatcher(msgType='group', id='871835811', hour='17', minute='7', desc='非遗3')
@cronMatcher(msgType='group', id='871835811', hour='11', minute='45', desc='非遗3')
async def main():
	yield [
		Text('@全体成员 @献给已逝公主の混沌古神 睡在蕾咪床底被咲夜杀了\n'),
		Image(path=Path(__file__).parent / 'sakuya.png'),
		Text('——来自群管理员（2665924795）的编辑'),
	]