from enum import Enum

class TargetType(Enum):
	PRIVATE = "private"
	GROUP = "group"

class Target:
	def __init__(self, targetType: TargetType|str, id: str|list[str]):
		if type(targetType) == str:
			targetType = TargetType(targetType)
		self.type = targetType
		self.id = id