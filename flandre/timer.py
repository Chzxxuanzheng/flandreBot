from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.rule import Rule

from .event import backendHandOutEvent

class _TimerManager(AsyncIOScheduler):
	startFlag = False
	def start(self):
		if self.startFlag:return
		super().start()
		self.startFlag = True

	def stop(self):
		self.shutdown()

	def registerTimeEvent(self, **kwargs)-> Rule:
		from flandre.event import TimeEvent
		if not (id := kwargs.get('id', None)):
			raise ValueError('id must be provided for the job')
		if not (trigger := kwargs.get('trigger', None)):
			raise ValueError('trigger must be provided for the job')
		if trigger not in ['cron', 'interval']:
			raise ValueError('trigger must be cron or interval')
		async def rule(event: TimeEvent)->bool:
			return event.id == id
		
		if trigger == 'cron':
			argks = [
				'second', 'minute', 'hour', 'day',
				'day_of_week', 'week', 'month', 'year',
				'start_date', 'end_date'
			]
		else:
			argks = [
				'seconds', 'minutes', 'hours', 'days',
				'months', 'years', 'start_date', 'end_date'
			]
		kwargs = {k: kwargs[k] for k in argks if k in kwargs}
		if not kwargs:
			raise ValueError(f'kwargs error for trigger {trigger}')
		async def createEvent():
			backendHandOutEvent('timer', TimeEvent(
				trigger=trigger,
				id=id,
				**kwargs,
			))

		self.add_job(createEvent, 
			trigger=trigger,
			id=id,

			**kwargs,
		)
		return Rule(rule)
	
timerManager = _TimerManager()

from nonebot import get_driver
@get_driver().on_startup
async def on_bot_connect():
	timerManager.start()
@get_driver().on_shutdown
async def on_shutdown():
	timerManager.stop()