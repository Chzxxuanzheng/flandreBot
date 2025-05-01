from util import baseConfig, BaseModel

class Rcon(BaseModel):
	host: str
	port: int
	passwd: str

class Forward(BaseModel):
	chatInfoUrl: str
	groups: dict[int, str]
	sleepTime: float
	afterSendSleepTime: float
	reconnectTime: float

class Config(baseConfig('minecraft')):
	"""Plugin Config Here"""
	rcon: Rcon
	forward: Forward

config = Config.getConfig()