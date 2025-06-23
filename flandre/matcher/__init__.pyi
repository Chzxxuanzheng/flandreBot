from typing import Literal

from nonebot_plugin_alconna import Target, SupportScope

from flandre.typing import ScopeLiteral

from .commandMatcher import commandMatcher as commandMatcher
from .connectMatcher import connectMatcher as connectMatcher
from .errorMatcher import matcherErrorMatcher as matcherErrorMatcher
from .regexMatcher import regexMatcher as regexMatcher
from .timerMatcher import intervalMatcher as intervalMatcher, cronMatcher as cronMatcher
from .messageMatcher import messageMatcher as messageMatcher

def target(msgType: Literal['group','private'], id: int|str, platform: ScopeLiteral|SupportScope = ...)-> Target:...

class Finish:
	'''
	用于标记处理器结束
	用法：
	```python
	yield Finish('结束处理')
	```
	类似于下面的含义
	```python
	await finish('结束处理')
	```
	'''
	def __init__(self, msg):...