from nonebot import logger
import httpx
import asyncio
from typing import AsyncGenerator, Optional
from json import loads
from .model import AiData, AiMessage

from enum import Enum
class RespStatus(str, Enum):
	OK = 'ok'
	ERROR = 'error'
	Done = 'done'

class Lock:
	__locks = {}
	def __init__(self, id: Optional[str]=None):
		if id:
			self.lock: asyncio.Lock = Lock.__locks.setdefault(id, asyncio.Lock())

	async def __aenter__(self):
		if hasattr(self, 'lock'):
			await self.lock.__aenter__()
	
	async def __aexit__(self, exc_type, exc_val, exc_tb):
		if hasattr(self, 'lock'):
			await self.lock.__aexit__(exc_type, exc_val, exc_tb)

class RespData:
	data: AiData|None = None
	type: RespStatus
	error: None|Exception = None

	def __init__(self, response: str):
		self.data = None
		self.error = None
		# 解析响应字符串，提取出内容
		if response.startswith('data: '):
			response = response[6:]
		else:
			self.type = RespStatus.ERROR
			self.error = Exception(f'数据格式错误:{response}')
			return
		if response == '[DONE]':
			self.type = RespStatus.Done
		else:
			try:
				self.type = RespStatus.OK
				self.data = AiData(**loads(response))
			except Exception as e:
				from json import dumps
				print(dumps(loads(response), indent=2, ensure_ascii=False))
				self.type = RespStatus.ERROR
				self.error = e


	def __call__(self)-> str|None:
		if not self.data:return None
		if not self.data.choices:return None
		if not self.data.choices[0].delta:return None

		return self.data.choices[0].delta.content


if __name__ == '__main__':
	# api = 'https://api.aionline.fun'
	api = 'https://api.v3.cm'
	# key = 'sk-itoStfhA8wWAueuPDHr7SaFHGXdDMX7sYJLg3e37RmQ2mPJD'
	key = 'sk-QDNPeJyHTOIDAQ9r533e3b0e41A74b45B14bF55114C536B5'
	gpt = 'gpt-3.5-turbo'
	claude = 'claude-3-haiku-20240307'
else:
	from .config import config
	api = config.api
	key = config.key
	gpt = config.gptModel
	claude = config.claudeModel

__locks = {}  # 用于存储锁的字典

class Fetch:
	headers: dict[str, str] = {
		"Authorization": f'Bearer {key}',
		"Content-Type": "application/json"
	}
	url = f'{api}/v1/chat/completions'

	def __init__(self, model: str, content: AiMessage, lock: Optional[str]=None):
		logger.info(content.model_dump())
		self.data = {
			'model': model,
			'messages': content.model_dump(),
			"stream": True  # 开启流式输出
		}
		self.lock: Lock = Lock(lock)

	async def read(self) -> str:
		async with self.lock:
			return '\n'.join([i async for i in self.__fetch(self.url)])
			
	async def stream(self) -> AsyncGenerator[str, None]:
		async with self.lock:
			async for i in self.__fetch(self.url):
				if i:yield i

	async def __fetch(self, url: str) -> AsyncGenerator[str, None]:
		async with httpx.AsyncClient(timeout=10) as client:
				cache = ''
				async with client.stream("POST", url, headers=self.headers, json=self.data) as resp:
					if resp.status_code == 200:
						# 流式读取响应
						async for line in resp.aiter_lines():
							if not line.strip():continue
							data = RespData(line)
							if data.type == RespStatus.Done:
								break
							elif data.type == RespStatus.ERROR:
								logger.error(f'解析错误:{data.error}')
								continue
							elif data.type == RespStatus.OK:
								content = data()
								if not content:continue
								for i in content:
									if i == '\n':
										yield cache
										cache = ''
									else:
										cache += i
					else:
						raise Exception(f'请求失败,状态码:{resp.status_code},内容:{loads((await resp.aread()))}')

		if cache:
			yield cache
	

async def useGpt(content: AiMessage) -> str|None:
	return await Fetch(gpt,content).read()

async def useC(content: AiMessage, id: str) -> AsyncGenerator[str, None]:
	lock = __locks.setdefault(id, asyncio.Lock())
	async with lock:  # 同步执行相同 id 的请求
		async for response in Fetch(claude, content, id).stream():
			yield response