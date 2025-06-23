from .config import config
from nonebot import logger
from datetime import datetime

import httpx

from flandre import commandMatcher
from flandre.annotated import plaintextArg

from uuid import uuid4

@commandMatcher('kd', desc='kd翻译')
async def main(arg: str = plaintextArg()):
	logger.info(f"Received translation request: {arg}")
	try:
		yield await translate(arg)
	except Exception as e:
		yield "翻译失败"
		raise e

async def translate(text: str) -> str:
	async with httpx.AsyncClient() as client:
		data = {
			'q': text,
			'from': 'auto',
			'to': 'zh-CHS',
			'appKey': config.id,
			'salt': uuid4().hex,
			'curtime': int(datetime.now().timestamp())
		}
		sign(data)
		response = await client.get(
			'https://openapi.youdao.com/api',
			params=data
		)
		response.raise_for_status()
		data = response.json()
		if data['errorCode'] == '0':
			return data['translation'][0]
		else:
			logger.error(f"Translation error: {data['msg']}")
			return f"Error: {data['msg']}"

def sign(data: dict):
	from hashlib import sha256
	originData = data.copy()
	if len(data['q']) > 20:
		originData['q'] = originData['q'][-10:]
	data['signType'] = 'v3'
	data['sign'] = sha256(f"{originData['appKey']}{originData['q']}{originData['salt']}{originData['curtime']}{config.key}".encode('utf-8')).hexdigest()