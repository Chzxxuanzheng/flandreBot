from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from nonebot import logger
from nonebot_plugin_orm import get_session
from sqlalchemy import select, desc
from asyncio import TaskGroup

# from .gpt import useGpt, useC
# from .config import Config

# from util.send import getId, createMd, createButton, toOffical
# from util.button import Button
from .model import AiMessage, AiContent, OrmContent
from .orm import ChatData
from .config import config
from util.rule import norRule
from core.matcher import commandMatcher

from .useAi import useGpt, useC

# 定义了一个处理gpt命令的函数，使用norRule作为规则
@commandMatcher('gpt', 'GPT', 'Gpt', rule=norRule, desc='使用GPT')
async def gpt(event: MessageEvent, args: Message = CommandArg()):
 msg = event.message_id
 user = event.sender.nickname
 if not (args := args.extract_plain_text()):
  yield Message([MessageSegment.reply(msg), MessageSegment.text('您需要问gpt什么问题？')])
  return
 context = await __createContexts(__getId(event), 'gpt')
 context.append(__userContext(user, args))
 try:
  out = await useGpt(context)
 except Exception as e:
  logger.error(e)
  yield Message([MessageSegment.reply(msg), MessageSegment.text('gpt错误')])
  return
 if out == None:
  yield Message([MessageSegment.at(2431149266), MessageSegment.text('gpt错误')])
 
 logger.info(out)
 await __addHistory(__getId(event), 'gpt', OrmContent(role='user', content=args, user=user))
 await __addHistory(__getId(event), 'gpt', OrmContent(role='assistant', content=out))
 send = Message([MessageSegment.reply(msg), MessageSegment.text(out)])
 yield send


# 定义了一个清除gpt上下文的函数
@commandMatcher('gpt清除上下文', 'GPT清除上下文', 'Gpt清除上下文', rule=norRule, desc='清除GPT上下文')
async def clearContext(event: MessageEvent):
 await __clearHistory(__getId(event), 'gpt')
 yield Message([MessageSegment.reply(event.message_id),'上下文已清除'])

# 创建上下文信息
async def __createContexts(id: int, model: str) -> AiMessage:
 context = await __getHistory(id, model)
 context.append(__context(config.exSetting, 'system'))
 return context

# 获取历史聊天记录
async def __getHistory(id: int, model: str) -> AiMessage:
 session = get_session()
 async with session.begin():
  history = (await session.scalars(
   select(ChatData)
   .where(ChatData.id == id and ChatData.model == model)
   .order_by(desc(ChatData.date))
   .limit(config.contextLong)
  )).all()
  return AiMessage(history)

# 添加聊天记录到数据库
async def __addHistory(id: int, model: str, data: OrmContent) -> None:
 session = get_session()
 async with session.begin():
  history = ChatData(id=id, data=data, model=model)
  session.add(history)
  await session.commit()

# 清除指定用户的聊天记录
async def __clearHistory(id: int, model: str) -> None:
 session = get_session()
 async with session.begin():
  history = (await session.scalars(
   select(ChatData)
   .where(ChatData.id == id and ChatData.model == model)
   .order_by(desc(ChatData.date))
  )).all()
  async with TaskGroup() as tg:
   for i in history: tg.create_task(session.delete(i))
  await session.commit()

# 创建用户聊天内容
def __userContext(user: str, content: str) -> AiContent:
 return __context(f'{user}:\n{content}', 'user')

# 创建AiContent对象
def __context(content: str, role: str = 'user') -> AiContent:
 # 这里是创建一个AiContent对象
 if role not in ['user', 'assistant', 'system']:
  raise ValueError(f"非法的role参数({role}). 必须是'user' 'assistant' 'system'.")
 return AiContent(role=role, content=content)

# 获取用户或群组的id
def __getId(event: MessageEvent) -> int:
 # 这里是获取id的函数
 if isinstance(event, GroupMessageEvent):
  return event.group_id
 else:
  return event.user_id
# gpt = on_command("gpt", aliases=set(['GPT', 'Gpt']), rule=norRule)
# c = on_command("c", aliases=set(['C']), rule=norRule)
# cCharaSetting = on_command("c人设", aliases=set(['C人设']), rule=norRule)
# cDefaultSetting = on_command("c默认人设", aliases=set(['C默认人设']), rule=norRule)
# cResetSetting = on_command("c重置人设", aliases=set(['C重置人设']), rule=norRule)
# cRemoveMember = on_command("c清除上下文", aliases=set(['C清除上下文']), rule=norRule)

# gpt4 = on_command('gpt4', rule=norRule)

# @gpt.handle()
# async def _(args: Message = CommandArg()):
# 	args = args.extract_plain_text()
# 	await gpt.finish(f'gpt被更适合聊天的claude取代,请使用 c{args}')

# @gpt4.handle()
# async def useGpt4(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
# 	msg = event.message_id
# 	user = event.sender.nickname
# 	if not (args := args.extract_plain_text()):
# 		await gpt4.finish('没有内容')
# 	out = useGpt(args, {"role": "user", "content": args}, user)
# 	logger.info(out)
# 	if out == None:
# 		await c.finish(MessageSegment.at(2431149266) + 'gpt4错误')
# 	else:
# 		# md = createMd(out)
# 		# await c.send(Message([md]))
# 		send = Message([MessageSegment.reply(msg), MessageSegment.text(out)])
# 		await c.send(send)

# #信息收集
# @c.handle()
# async def out(event: MessageEvent, bot: Bot, args: Message = CommandArg()):
# 	msg = event.message_id
# 	user = event.sender.nickname
# 	if not (args := args.extract_plain_text()):
# 		await menu(event, bot)
# 	out = useC(args, createContent(event), user)
# 	logger.info(out)
# 	if out == None:
# 		await c.finish(MessageSegment.at(2431149266) + 'claude错误')
# 	else:
# 		contentUpdate(event, user, args, out)
# 		# md = createMd(out)
# 		# await c.send(Message([md]))
# 		send = Message([MessageSegment.reply(msg), MessageSegment.text(out)])
# 		await c.send(send)

# # 总设置
# async def menu(event: MessageEvent, bot: Bot):
# 	charaSetting = getContent(event)
# 	charaSetting = '\n'.join(f'> {i}' for i in charaSetting.split('\n'))
# 	info = f'# claude设置\n ### 当前人设:\n{charaSetting}'
# 	md = createMd(info)
# 	reset = Button('重置人设', 'c重置人设')
# 	setChara = Button('设置人设', 'c人设 (把这里换成人设)', False)
# 	default = Button('默认人设', 'c默认人设')
# 	clear = Button('清除上下文', 'c清除上下文')
# 	chart = Button('聊天', 'c (说些什么吧?)', False)
# 	buttons = createButton([[reset,setChara],[default,clear],[chart]])
# 	# await c.finish(Message([md,buttons]))
# 	await c.finish('md被tx吃了,不支持')

# # 管理设置
# @cCharaSetting.handle()
# async def out(event: MessageEvent, args: Message = CommandArg()):
# 	if not (args := args.extract_plain_text()):
# 		await cCharaSetting.finish(f'claude人设:\n{getContent(event)}')
# 	else:
# 		resetContent(event)
# 		setContent(event, args)
# 		await cCharaSetting.send("claude人设已更新")
# 		await removeMember(event)

# # 默认人设
# @cDefaultSetting.handle()
# async def out():
# 	await cDefaultSetting.finish(Config.defaultText())


# @cResetSetting.handle()
# async def out(event: MessageEvent):
# 	resetContent(event)
# 	await cDefaultSetting.send("已重置人设")
# 	await removeMember(event)

# @cRemoveMember.handle()
# async def removeMember(event: MessageEvent):
# 	removeContent(event)
# 	await cDefaultSetting.send("已清除上下文")

# def getContent(event: MessageEvent)->str:
# 	id = getId(event)
# 	with sqlite3.connect('setting.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptSetting'")
# 		if not cur.fetchone():
# 			return Config.defaultText()
# 		cur.execute(f"SELECT content FROM gptSetting WHERE id={id}")
# 		out = cur.fetchone()
# 		if out:
# 			return out[0]
# 	return Config.defaultText()

# def setContent(event: MessageEvent, content: str):
# 	id = getId(event)
# 	content = content.replace('\'','\'\'')
# 	with sqlite3.connect('setting.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptSetting'")
# 		if not cur.fetchone():
# 			cur.execute('''CREATE TABLE gptSetting
#            (content TEXT,
#             id NUMBER);''')
# 		cur.execute(f"INSERT INTO gptSetting VALUES('{content}', {id})")

# def resetContent(event: MessageEvent):
# 	id = getId(event)
# 	with sqlite3.connect('setting.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptSetting'")
# 		if not cur.fetchone():
# 			return
# 		cur.execute(f"DELETE FROM gptSetting WHERE id={id};")

# def createContent(event: MessageEvent)-> list:
# 	out = [{"role": "system", "content": getContent(event)},]
# 	id = getId(event)
# 	with sqlite3.connect('data.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptContent'")
# 		if not cur.fetchone():
# 			return out
# 		cur.execute(f"SELECT * FROM gptContent WHERE id={id}")
# 		member = cur.fetchall()[::-1]
# 		taken = 0
# 		tmp = []
# 		for i in member:
# 			taken += len(i[2])
# 			if taken >= 1024:
# 				break
# 			tmp.append({'role': i[1], 'content': i[2]})
# 		out.extend(tmp[::-1])
# 		return out

# def contentUpdate(event: MessageEvent, user: str, question: str, out: str):
# 	id = getId(event)
# 	user = user.replace('\'','\'\'')
# 	question = question.replace('\'','\'\'')
# 	out = out.replace('\'','\'\'')
# 	with sqlite3.connect('data.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptContent'")
# 		if not cur.fetchone():
# 			cur.execute(f'''CREATE TABLE gptContent
#            (id NUMBER,
# 			send TEXT,
# 			content TEXT);''')
# 		logger.info(f"INSERT INTO gptContent VALUES({id}, 'user', '{user}:\n{question}')")
# 		cur.execute(f"INSERT INTO gptContent VALUES({id}, 'user', '{user}:\n{question}')")
# 		cur.execute(f"INSERT INTO gptContent VALUES({id}, 'assistant', '{out}')")

# def removeContent(event: MessageEvent):
# 	id = getId(event)
# 	with sqlite3.connect('data.db') as conn:
# 		cur = conn.cursor()
# 		cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='gptContent'")
# 		if not cur.fetchone():
# 			return out
# 		cur.execute(f"DELETE FROM gptContent WHERE id={id}")