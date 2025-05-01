from nonebot.adapters.onebot.v11 import MessageSegment
from core import cronMatcher

@cronMatcher(msgType='group', id='871835811', hour='11', minute='45', desc='非遗3')
async def main():
	msg = []
	msg.append(MessageSegment.text('@全体成员 @献给已逝公主の混沌古神 睡在蕾咪床底被咲夜杀了\n'))
	with open(r'/home/lee/project/qBot/nb/plugins/tohoschedule/sakuya.png', 'rb')as f:
		msg.append(MessageSegment.image(f.read()))
	yield msg
