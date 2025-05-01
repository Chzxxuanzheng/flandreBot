from nonebot.adapters.onebot.v11 import MessageSegment
from core import cronMatcher

@cronMatcher(msgType='group', id='871835811', hour='16', minute='0', desc='非遗1')
async def main():
	msg = []
	msg.append(MessageSegment.text('@全体成员'))
	msg.append(MessageSegment.text(" 我们群主敢日八云紫！\n"))
	with open(r'/home/lee/project/qBot/nb/plugins/tohoschedule/yokari.png', 'rb')as f:
		msg.append(MessageSegment.image(f.read()))
	msg.append(MessageSegment.text("——来自群管理员（2665924795）的编辑"))
	yield msg
