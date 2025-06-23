from types import TracebackType
from typing import Any, AsyncGenerator, Callable, Coroutine
from nonebot_plugin_alconna.uniseg import Target
from flandre.message import Msg, toUniMsg

type Handler = Callable[[Any], AsyncGenerator[None|Msg,None]]
type Sender = Callable[[Handler, Any], Coroutine[None, None, None]]

# 钩子返回值
type HandlerRet = Msg|Finish|Target|None


class HandlersManager:
	def __init__(self, agen: AsyncGenerator[HandlerRet, Any] | None = None):
		if agen is None:
			raise ValueError('agen must be an AsyncGenerator or async generator function')
		self.nowAgen: AsyncGenerator[HandlerRet, Any] = agen
		self.result: HandlerRet | None = None
		self.stack: list[AsyncGenerator[HandlerRet, Any]] = []
		self.finishFlag: bool = False


	def __aiter__(self) -> AsyncGenerator[HandlerRet, Any]:
		# 通常情况
		if isinstance(self.nowAgen, AsyncGenerator):
			return self
		elif isinstance(self.nowAgen, Coroutine):
			# 无返回值特殊情况
			async def tmp():
				await self.nowAgen # type: ignore
				yield
			return tmp()
		else:
			raise TypeError(f'nowAgen must be AsyncGenerator or async generator function, but got {type(self.nowAgen)}')


	async def __anext__(self) -> HandlerRet:
		# 优先返回缓存结果
		if self.result != None:
			re = self.result
			self.result = None
			return re
		if self.finishFlag:raise StopAsyncIteration
		
		try:

			# 如果当前异步生成器存在，则从中获取下一个值
			re = await self.nowAgen.__anext__()
			if isinstance(re, AsyncGenerator):
				# 如果返回值是异步生成器，则将其设置为当前异步生成器
				self.stack.append(self.nowAgen)
				self.nowAgen = re
				return await self.__anext__()
			elif isinstance(re, Coroutine):
				re = await re
			return re
		except StopAsyncIteration:
			self.__stopCheck()
			return await self.__anext__()


	async def asend(self, msg: Any) -> None:
		try:
			'''向当前异步生成器发送消息'''
			self.result = await self.nowAgen.asend(msg)
		except StopAsyncIteration:
			# 如果当前异步生成器结束，则从栈中弹出上一个异步生成器
			self.__stopCheck()

	async def athrow(self, typ: type[BaseException]|BaseException, val: BaseException | object | None = None, tb: TracebackType | None = None) -> None:
		try:
			'''向当前异步生成器抛出异常'''
			if isinstance(typ, BaseException):
				self.result = await self.nowAgen.athrow(typ)
			else:
				self.result = await self.nowAgen.athrow(typ, val, tb)
		except StopAsyncIteration:
			# 如果当前异步生成器结束，则从栈中弹出上一个异步生成器
			self.__stopCheck()

	async def aclose(self) -> None:
		if self.finishFlag:
			return
		if isinstance(self.nowAgen, AsyncGenerator):
			await self.nowAgen.aclose()
		self.__stopCheck()
		return await self.aclose()

	def __stopCheck(self):
		# 如果当前异步生成器结束，则从栈中弹出上一个异步生成器
		if self.stack:
			self.nowAgen = self.stack.pop()
		else:
			# 如果栈为空，则抛出StopAsyncIteration异常
			self.finishFlag = True


class Finish:
	def __init__(self, *msg: Msg):
		if len(msg) == 0:
			self.msg = None
		else:
			self.msg = toUniMsg(*msg)


class RecallMsg:
	def __init__(self, id: int):
		'''
		:param id: 要撤回的消息的id，该ID为在**事件响应函数**中发送的消息顺序，**而非**message_id
		'''
		self.id = id
	

def createSender(defaultTarget: Target|None)-> Sender:
	tmp = []
	async def sender(handler: Handler, *args, **kwargs)-> None:
		nowTarget: Target|None = defaultTarget
		agenManager = HandlersManager(handler(*args, **kwargs))
		finish = False
		needSend: Msg|None = None
		async for msg in agenManager:
			tmp.append(msg)
			if not msg:continue
			re = None

			# 信息条分
			if isinstance(msg, Target):
				nowTarget = msg
			elif isinstance(msg, Finish):
				needSend = msg.msg
				finish = True
			else:
				needSend = msg

			# 发送消息
			try:
				if needSend:
					re = await send(nowTarget, needSend)
					needSend = None
			except Exception as e:
				await agenManager.athrow(e)
			else:
				if finish:break

				await agenManager.asend(re)
				re = None
	
	return sender

async def send(target: Target|None, msg: Msg|None = None) -> None:
	'''
	发送消息
	:param target: 目标
	:param msg: 消息内容
	'''
	if not msg:
		return
	if not target:
		raise ValueError('target is needed')

	await target.send(toUniMsg(msg))