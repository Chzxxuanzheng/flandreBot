from nonebot.adapters.milky import MessageSegment
from flandre import cronMatcher
from pathlib import Path

@cronMatcher(msgType='group', id='871835811', hour='11', minute='45', desc='非遗3')
# @cronMatcher(msgType='group', id='871835811', hour='17', minute='7', desc='非遗3')
async def main():
	msg = []
	msg.append(MessageSegment.text('@全体成员 @献给已逝公主の混沌古神 睡在蕾咪床底被咲夜杀了\n'))
	msg.append(MessageSegment.image(path=Path(__file__).parent / 'sakuya.png'))
	yield msg
