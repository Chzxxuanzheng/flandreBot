from core.matcher import commandMatcher

@commandMatcher('ping', 'p', desc='ping')
async def ping():
	yield 'pong'