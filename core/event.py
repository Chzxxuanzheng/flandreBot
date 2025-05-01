from nonebot.adapters import Message
from nonebot.adapters import Event as BaseEvent
from nonebot.drivers import Driver
from typing import override
from abc import abstractmethod
from datetime import datetime
from .matcher.exMatcher import ExMatcher
from .target import Target

class EmitEvent(BaseEvent):
	"""
	Matcher委托事件
	"""
	name: str
	def __init__(self, *args, matcher: ExMatcher, target: Target, **kwargs):
		super().__init__(*args, **kwargs)
		self.matcher = matcher
		self.target = target

	@override
	def get_type(self) -> str:
		return 'meta_event'
	
	@override
	def get_event_name(self) -> str:
		"""获取事件名称的方法。"""
		return f'meta_event.emit.{self.name}'

	@override
	def get_event_description(self) -> str:
		return f'<blue>(for {self.matcher})</blue>{self.desc()}'

	@abstractmethod
	def desc(self)->str:...

	@override
	def get_message(self) -> Message:
		raise ValueError("Event has no message!")

	@override
	def get_user_id(self) -> str:
		raise ValueError("Event has no context!")

	@override
	def get_session_id(self) -> str:
		raise ValueError("Event has no context!")

	@override
	def is_tome(self) -> bool:
		return False


class ConnectEvent(EmitEvent):
	"""
	连接协议层事件
	"""
	name: str = 'connect'

	def __init__(self, driver: Driver, time: datetime, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.driver = driver
		self.time = time

	@override
	def desc(self) -> str:
		"""获取事件描述的方法，通常为事件具体内容。"""
		return f'connect to {self.driver.type} at {self.time.strftime("%Y-%m-%d %H:%M:%S")}'


class TimeEvent(EmitEvent):
	"""
	定时任务
	"""
	name: str = 'time'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cornArgs = [
			'second',
			'minute',
			'hour',
			'day',
			'day_of_week',
			'week',
			'month',
			'year',
			'start_date',
			'end_date',
		]
		intervalArgs = [
			'seconds',
			'minutes',
			'hours',
			'days',
			'months',
			'years',
			'start_date',
			'end_date',
		]
		type = kwargs.get('trigger', None)
		if type not in ['cron', 'interval']:
			raise ValueError('trigger must be cron or interval')
		self.argDesc = ''
		if type == 'cron':
			for i in cornArgs:
				if i in kwargs.keys():
					self.argDesc += f'{i}={kwargs[i]}, '
			self.descStr = f'cron event triggered with {self.argDesc}'
		elif type == 'interval':
			for i in intervalArgs:
				if i in kwargs.keys():
					self.argDesc += f'{i}={kwargs[i]}, '
			self.descStr = f'interval event triggered every {self.argDesc}'

	@override
	def desc(self) -> str:
		"""获取事件描述的方法，通常为事件具体内容。"""
		return self.descStr
