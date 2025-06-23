from flandre import baseConfig

class Config(baseConfig('otp')):
	"""Plugin Config Here"""
	userId: int

config = Config.getConfig()