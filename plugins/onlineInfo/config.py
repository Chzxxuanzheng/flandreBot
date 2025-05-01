from util import baseConfig


class Config(baseConfig('onlineInfo')):
	"""Plugin Config Here"""
	info: str

config: Config = Config.getConfig()