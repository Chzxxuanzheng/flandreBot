from typing import cast
from nonebot.params import CommandArg
from nonebot.adapters.minecraft.bot import Bot
from nonebot import get_bot
from nonebot import logger

from flandre import commandMatcher, connectMatcher, Finish
from flandre.annotated import Uninfo, Arg
from flandre.rule import scope
from flandre.message import toPlaintext, reply

from util.rule import norRule

from .permissionCheck import checkAdmin

rule = norRule & scope('QQClient')

@commandMatcher('rcon', rule=rule, desc='执行rcon指令')
async def main(info: Uninfo, argMsg: Arg):
	yield checkAdmin(info)

	bot: Bot = cast(Bot, get_bot('Server'))

	arg = toPlaintext(argMsg)

	slashStart = False
	if not arg:
		yield Finish(
			reply(),
			'缺少指令',
		)
		return

	if arg[0] == '/':
		slashStart = True
		arg = arg[1:]

	resp = await bot.send_rcon_command(command=arg)

	if resp == '':
		resp = '[无返回结果]'
	elif resp == 'Unknown command. Type "/help" for help.':
		resp = '[无效指令]'
	logger.info(f'{info.user.id}执行`{arg}`，结果`{resp}`')
	yield reply(), resp
	if slashStart:
		yield '提示:rcon指令开头不需要添加/'