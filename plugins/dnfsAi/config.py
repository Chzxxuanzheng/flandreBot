from util import baseConfig


class Config(baseConfig("dnfsAi")):
	"""Plugin Config Here"""
	api: str
	key: str
	allowGroup: int
	system: str

config = Config.getConfig()