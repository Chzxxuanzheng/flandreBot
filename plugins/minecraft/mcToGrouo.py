from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger
from .config import config
import asyncio

# 要转发的群
GROUP_INFO: list[int] = config.forward.groups.keys()

# 定义服务器地址和端口
SERVER_URL = config.forward.chatInfoUrl

driver = get_driver()

from httpx import AsyncClient
import asyncio

__run = True

async def client(bot: Bot, sleep: float, sendSleep: float, reconnect: int = 10):
	while __run:
		try:
			async with AsyncClient() as client:
				# 发送消息到服务器
				resp = await client.get(SERVER_URL)
				if resp.status_code == 200:
					text = resp.text
					if text.strip() == "None":
						pass
					else:
						# 打印聊天消息
						logger.info(f'收到MC消息:{text}')
						for gid in GROUP_INFO:
							await bot.send_msg(message_type="group",group_id=gid,message=text)
						await asyncio.sleep(sendSleep)
				else:
					logger.error(f"HTTP code {resp.status_code}")
				# sleep
				await asyncio.sleep(sleep)
		except asyncio.CancelledError:
			...
		except Exception as e:
			logger.error(f"Error: {e}")
			await asyncio.sleep(reconnect)

# 主函数用于持续轮询
async def main(bot: Bot):
	# 启动异步客户端
	await client(bot, config.forward.sleepTime, config.forward.afterSendSleepTime, config.forward.reconnectTime)

async def _start(bot: Bot):
	await main(bot)

async def _stop():
	global __run
	__run = False
	logger.info('停止信号已发出')

driver.on_bot_connect(_start)
driver.on_shutdown(_stop)