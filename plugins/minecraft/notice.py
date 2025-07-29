from flandre import noticeMatcher
from nonebot.rule import Rule
from nonebot.adapters.minecraft.event.base import BaseJoinEvent
from nonebot.adapters.minecraft.event.spigot import PlayerJoinEvent
from nonebot_plugin_alconna.uniseg import Target, SupportScope

from .config import config

async def rule(event: BaseJoinEvent):
	print(f'玩家 {event.player.nickname} 加入游戏')
	return True

@noticeMatcher(desc='Mc加入游戏提示', rule=Rule(rule), priority=20, block=False)
async def forward(event: BaseJoinEvent):
	for group in config.forward.groups.keys():
		yield Target.group(str(group), SupportScope.qq_client)
		yield joinMsg(event.player.nickname)

def joinMsg(name: str) -> str:
	from random import choice
	list = [
		'{name}穿越到了方块世界～',
		'{name}打开了Minecraft，还有人要来玩吗？',
		'{name}开始钻研挖矿与工艺了',
		'{name}进入了Minecraft的世界，准备开始冒险',
		'{name}打开了MC！大伙快来玩',
	]
	return choice(list).format(name=name)