from core import commandMatcher, finish, messageMatcher, FinishMatcherProcess, RecallMsg
from util.rule import norRule, fromGroup, to_me
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot_plugin_orm import async_scoped_session
from httpx import ReadTimeout, RemoteProtocolError
from sqlalchemy import select
from .orm import ConversationId

from .config import config
from .useAi import Fetch, StatusError
from .md import betterMd

fetch = Fetch()

@messageMatcher(desc='在dnfs社区群内调用他们的AI', priority=10, rule=to_me() & fromGroup(config.allowGroup))
async def ai(event: MessageEvent, session: async_scoped_session):
	# 获取消息
	question = event.get_plaintext()
	if event.reply:
		reply = event.reply.message.extract_plain_text()
		user = event.reply.sender.nickname
		if not user: user = f'未知用户({event.reply.sender.user_id})'
		question = f'```reply\n{user}:\n{reply}```\n{question}'
	if not question:
		finish([MessageSegment.reply(event.message_id), "请输入问题"])
	user = event.sender.nickname
	if not user: user = f'未知用户({event.user_id})'

	async with session.begin():
		getId = (await session.scalars(select(ConversationId))).first()
		if getId: conversation_id = getId.id
		else: conversation_id = None

	# 询问AI
	try:
		thinking = False
		async for resp in fetch(question, user, conversation_id):
			if not thinking:
				thinking = True
				yield [MessageSegment.reply(event.message_id), "正在思考..."]
		if thinking: yield RecallMsg(0)
		if not resp: finish([MessageSegment.reply(event.message_id), "回复为空"])
		answers, conversation_id = resp
		answers.reverse()
		for answer in answers:
			answer = answer.split('</think>').pop().replace('Final Answer:', '').strip()
			if answer:break
		else:
			finish([MessageSegment.reply(event.message_id), '回复为空'])

		parse = answer.split('</details>')
		yield [MessageSegment.reply(event.message_id), *await betterMd(parse[0])]
		async with session.begin():
			getId = (await session.scalars(select(ConversationId))).first()
			if not getId:
				session.add(ConversationId(id=conversation_id))
			await session.commit()
	except StatusError as e:
		finish([MessageSegment.reply(event.message_id), str(e)])
	except (TimeoutError, ReadTimeout) as e:
		finish([MessageSegment.reply(event.message_id), "请求超时"])
	except RemoteProtocolError:
		finish([MessageSegment.reply(event.message_id), "连接失败"])
	except FinishMatcherProcess:
		raise
	except Exception as e:
		yield [MessageSegment.reply(event.message_id), "未知错误"]
		raise e

@commandMatcher('ai清除上下文', 'ai清空上下文', 'ai重置上下文', desc='清除dnfs社区群内的AI上下文', rule=fromGroup(config.allowGroup) & norRule)
async def ai_clear(event: MessageEvent, session: async_scoped_session):
	async with session.begin():
		getId = (await session.scalars(select(ConversationId))).first()
		if getId:
			await session.delete(getId)
			await session.commit()
			finish([MessageSegment.reply(event.message_id), "已清除上下文"])
		else:
			finish([MessageSegment.reply(event.message_id), "上下文不存在"])