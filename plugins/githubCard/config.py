from util import baseConfig


class Config(baseConfig("githubCard")):
	"""Plugin Config Here"""
	proxy: str|None = None

config = Config.getConfig()