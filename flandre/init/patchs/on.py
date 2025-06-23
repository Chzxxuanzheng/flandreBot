from importlib import import_module

onModule = import_module('nonebot.plugin.on')
originOn = onModule.on

def patchOn(
	type: str = "",
    rule = None,
    permission = None,
	**kwargs
):
	matcher = originOn(
		type = type,
		rule = rule,
		permission = permission,
		handlers = kwargs.pop('handlers', None),
		expire_time = kwargs.pop('expire_time', None),
		priority = kwargs.pop('priority', 1),
		state = kwargs.pop('state', None),
		block = kwargs.pop('block', False),
		temp = kwargs.pop('temp', False),

		_depth = kwargs.pop('_depth', 0) + 1,
	)
	matcher.defaultTarget = kwargs.pop('defaultTarget', None)
	matcher.desc = kwargs.pop('desc', None)
	if not matcher.desc:
		raise ValueError('Matcher必须提供描述信息')
	return matcher

import_module('nonebot').on = patchOn # type: ignore
import_module('nonebot.plugin').on = patchOn # type: ignore
import_module('nonebot.plugin.on').on = patchOn # type: ignore