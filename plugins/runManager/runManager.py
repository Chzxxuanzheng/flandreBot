from nonebot.permission import SUPERUSER
from flandre.matcher import commandMatcher
from os import kill, getpid
from signal import SIGINT

from util.rule import norRule

@commandMatcher('关机', 'poweroff', 'shutdown',permission=SUPERUSER , desc='关机指令')
async def poweroff():
	yield '执行关机...'
	kill(getpid(), SIGINT)