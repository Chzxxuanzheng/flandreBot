from nonebot.internal.matcher.matcher import MatcherMeta, Matcher
import importlib
from typing import override, ClassVar
class ExMatcherMeta(MatcherMeta):
	@override
	def __repr__(self) -> str:
		return (
			f"{self.__name__}(desc={self.desc}"
			+ (f", module={self.module_name}" if self.module_name else "")
			+ (
				f", lineno={self._source.lineno}"
				if self._source and self._source.lineno is not None
				else ""
			)
			+ ")"
		)

class ExMatcher(Matcher, metaclass=ExMatcherMeta):
	desc: ClassVar[str] = ''
	@override
	def __repr__(self) -> str:
		return (
			f"{self.__class__.__name__}(desc={self.desc}"
			+ (f", module={self.module_name}" if self.module_name else "")
			+ (
				f", lineno={self._source.lineno}"
				if self._source and self._source.lineno is not None
				else ""
			)
			+ ")"
		)

onModule = importlib.import_module('nonebot.plugin.on')
onModule.Matcher = ExMatcher
