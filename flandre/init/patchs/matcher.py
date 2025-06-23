from nonebot.internal.matcher.matcher import MatcherMeta, Matcher
from importlib import import_module
from typing import override, ClassVar, TYPE_CHECKING
if TYPE_CHECKING:
	from nonebot_plugin_alconna.uniseg import Target
class PatchMatcherMeta(MatcherMeta):
	@override
	def __repr__(self) -> str:
		return (
			f"{self.__name__}(desc={self.desc}" # type: ignore
			+ (f", module={self.module_name}" if self.module_name else "")
			+ (
				f", lineno={self._source.lineno}"
				if self._source and self._source.lineno is not None
				else ""
			)
			+ ")"
		)

class PatchMatcher(Matcher, metaclass=PatchMatcherMeta):
	defaultTarget: 'ClassVar[Target|None]' = None
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

originMatcher = import_module('nonebot.internal.matcher.matcher').Matcher
import_module('nonebot.plugin.on').Matcher = PatchMatcher  # type: ignore
import_module('nonebot.internal.matcher.matcher').Matcher = PatchMatcher # type: ignore