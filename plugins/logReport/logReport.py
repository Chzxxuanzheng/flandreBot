from core import matcherErrorMatcher
from core.event import MatcherErrorEvent

@matcherErrorMatcher(msgType='private', id=2431149266, desc='错误捕捉')
async def logReport(event: MatcherErrorEvent):
	yield f'执行{event.errMatcher}失败\n错误信息：{event.error}\n事件信息：{event.event}'