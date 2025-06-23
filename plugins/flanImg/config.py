from flandre import baseConfig


class Config(baseConfig('flanImg')):
	"""Plugin Config Here"""
	norPath: str
	sexPath: str
	maxSendNum: int = 3
	norCmd: list[str]
	sexCmd: list[str]
	
config = Config.getConfig()