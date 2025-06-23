from nonebot.adapters.milky import MessageSegment
from flandre import cronMatcher
from pathlib import Path

@cronMatcher(msgType='group', id='871835811', hour='16', minute='0', desc='非遗1')
# @cronMatcher(msgType='group', id='871835811', hour=17, minute=8, desc='非遗1')
async def main():
	msg = []
	msg.append(MessageSegment.text('@全体成员'))
	msg.append(MessageSegment.text(" 我们群主敢日八云紫！\n"))
	msg.append(MessageSegment.image(path=Path(__file__).parent / 'yokari.png'))
	msg.append(MessageSegment.text("——来自群管理员（2665924795）的编辑"))
	yield msg
