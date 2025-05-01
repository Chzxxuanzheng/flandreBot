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

	def __str__(self):
		if type(self.id) == list:
			return f"{self.type.value}[{','.join(self.id)}]"
		else:
			return f"{self.type.value}[{self.id}]"