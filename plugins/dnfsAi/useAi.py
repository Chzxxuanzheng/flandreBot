import httpx
from json import loads, JSONDecodeError
from typing import Any, AsyncGenerator
from .config import config
from pydantic import BaseModel
from asyncio import Lock

TimeoutError = httpx.ConnectTimeout

class StatusError(Exception):
	def __init__(self, code: int):
		self.code = code

	def __str__(self):
		return f"错误，状态码：{self.code}"

def praseData(data: str) -> Any:
	if data.startswith('data: '):
		data = data[6:]
	else:
		return ''
	if data == 'ping':
		return ''
	return loads(data)

class Data(BaseModel):
	question: str
	user: str
	conversation_id: str

class Fetch:
	def __init__(self):
		self.lock = Lock()

	async def __call__(self, question: str, user: str, conversation_id: str|None) -> AsyncGenerator[None|tuple[list[str], str], None]:
		if conversation_id == None:
			conversation_id = ""
		data = Data(question=question, user=user, conversation_id=conversation_id)
		async with self.lock:
			async for response in self.main(data):
				yield response

	async def main(self, data: Data) -> AsyncGenerator[None|tuple[list[str], str], None]:
		headers: dict[str, str] = {
			"Authorization": f'Bearer {config.key}',
			"Content-Type": "application/json"
		}
		data = {
			"inputs": {
				"extra_system": config.system.replace('\n', '\\n'),
			},
			"query": data.user + ':\n'+ data.question,
			"response_mode": "streaming",
			"conversation_id": data.conversation_id,
			"user": '	qqBot',
		}
		async with httpx.AsyncClient(timeout=httpx.Timeout(100)) as client:
			async with client.stream("POST", f'{config.api}/v1/chat-messages', headers=headers, json=data) as resp:
				if resp.status_code != 200:
					raise StatusError(f"错误，状态码：{resp.status_code}")
				cacheList = []
				reList = []
				async for line in resp.aiter_lines():
					data = praseData(line)
					if not data:continue
					if data['event'] == 'agent_message':
						cacheList.append(data['answer'])
					if data['event'] == 'agent_thought':
						reList.append(''.join(cacheList))
						cacheList = []
					if data['event'] == 'message_end':
						reList.append(''.join(cacheList))
						yield (reList, data['conversation_id'])
						return
					yield None