from util import baseConfig

class Config(baseConfig('ai')):
	"""Plugin Config Here"""
	api: str
	key: str
	gptModel: str
	claudeModel: str
	defaultCharacterSetting: str = '''背景:芙兰天下第一可爱,她是一个吸血鬼幼女/萝莉/少女,有着七色翅膀。
现在你将扮演芙兰的一只玩具小熊,趁主人不注意,登上了她的QQ。'''
	exSetting: str = '你现在作为api在QQ(一种社交平台)上调用。你收到消息会以`群友名:\n群友的话`的格式进行展示,你的消息不用遵守这个消息。QQ不支持md等富文本格式,你不能以md的格式回复消息'
	contextLong: int = 20	# 上下文长度

config: Config = Config.getConfig()