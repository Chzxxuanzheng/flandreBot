from core.matcher import commandMatcher
from os import kill, getpid
from signal import SIGINT

from util.rule import fromSu, norRule

@commandMatcher('关机', 'poweroff', 'shutdown', rule=norRule & fromSu, desc='关机指令')
async def poweroff():
	yield '执行关机...'
	kill(getpid(), SIGINT)