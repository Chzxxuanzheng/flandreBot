import httpx
from json import loads
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

	async def __call__(self, question: str, user: str, conversation_id: str|None) -> AsyncGenerator[dict, None]:
		if conversation_id == None:
			conversation_id = ""
		data = Data(question=question, user=user, conversation_id=conversation_id)
		async with self.lock:
			async for response in self.main(data):
				yield response

	async def main(self, data: Data) -> AsyncGenerator[dict, None]:
		headers: dict[str, str] = {
			"Authorization": f'Bearer {config.key}',
			"Content-Type": "application/json"
		}
		data = {
			"inputs": {},
			"query": data.user + ':\n'+ data.question,
			"response_mode": "streaming",
			"conversation_id": data.conversation_id,
			"user": 'qqBot',
		}
		async with httpx.AsyncClient(timeout=httpx.Timeout(100)) as client:
			async with client.stream("POST", f'{config.api}/v1/chat-messages', headers=headers, json=data) as resp:
				if resp.status_code != 200:
					raise StatusError(f"错误，状态码：{resp.status_code}")
				async for line in resp.aiter_lines():
					data = praseData(line)
					if not data:continue
					if data['event']=='agent_thought':
						yield data