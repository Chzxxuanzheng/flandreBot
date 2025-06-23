from typing import Callable, Coroutine
from asyncio import iscoroutinefunction, TaskGroup
from enum import Enum

class InitState(int, Enum):
	NbNoInit = 0
	AfterNbInit = 1
	AfterAdapter = 2
	AfterInitHook = 3
	AfterPluginLoader = 4

nowSate = InitState.NbNoInit

hooks = []
asyncHooks = []

type hook = Callable[[], None]
type asyncHook = Callable[[], Coroutine]

async def runInitHook():
	async with TaskGroup() as tg:
		for hook in asyncHooks:
			tg.create_task(hook())
	for hook in hooks:
		hook()

def onInit(func: hook | asyncHook):
	if iscoroutinefunction(func):
		asyncHooks.append(func)
	else:
		hooks.append(func)