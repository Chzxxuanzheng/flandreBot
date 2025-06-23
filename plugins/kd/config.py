from flandre import baseConfig


class Config(baseConfig("kd")):
	"""Plugin Config Here"""
	id: str
	key: str

config = Config.getConfig()