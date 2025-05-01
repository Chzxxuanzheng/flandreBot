from typing import Self, Type
from pydantic import BaseModel

class BaseConfig(BaseModel):
	@classmethod
	def getConfig(cls)->Self:...

def baseConfig(pluginName: str)-> Type[BaseConfig]:...