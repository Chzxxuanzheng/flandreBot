from mcrcon import MCRcon as __MCRcon
from .config import config
import re

__rcon = config.rcon

def removeFormat(input: str)->str:
	return re.sub(r'§[0-9a-fk-or]', '', input)

def rcon(cmd: str) -> str:
	with __MCRcon(__rcon.host, __rcon.passwd, __rcon.port) as mcr:
		return removeFormat(mcr.command(cmd).strip())
