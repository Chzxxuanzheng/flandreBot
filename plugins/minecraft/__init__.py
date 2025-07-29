from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="minecraft",
    description="一些mc相关的东西",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from .useRcon import *
from .forward import *
from .adminManager import *
from .notice import *
# from .auth import *
from .orm import *