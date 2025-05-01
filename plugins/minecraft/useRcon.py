from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import MessageSegment, MessageEvent
from nonebot import logger

from core import commandMatcher, finish

from .rcon import rcon as _rcon
from .permissionCheck import checkAdmin


@commandMatcher('rcon', desc='执行rcon指令')
async def main(event: MessageEvent, args: Message = CommandArg()):

	await checkAdmin(event)

	uid = event.user_id
	msg = event.message_id
	slashStart = False
	args = args.extract_plain_text()
	if not args:
		finish(Message([MessageSegment.reply(msg), MessageSegment.text('请输入指令')]))
	if args[0] == '/':
		slashStart = True
		args = args[1:]
	resp = _rcon(args)
	if resp == '':
		resp = '[无返回结果]'
	elif resp == 'Unknown command. Type "/help" for help.':
		resp = '[无效指令]'
	logger.info(f'{uid}执行`{args}`，结果`{resp}`')
	msg: Message = Message([MessageSegment.reply(msg), MessageSegment.text(resp)])
	if slashStart:
		msg.append(MessageSegment.text('\n提示:rcon指令开头不需要添加/'))
	finish(msg)