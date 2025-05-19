from core import regexMatcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from re import search
from nonebot import logger

from .config import config

pattern = r"(?:https?://)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"

def getUrl(txt: str) -> str | None:
    """获取github项目链接（只保留github.com/owner/repo）"""
    # 匹配 http(s)://github.com/owner/repo 或 github.com/owner/repo
    m = search(pattern, txt)
    if m:
        return m.group(1), m.group(2)
    return None

@regexMatcher(pattern, desc='github连接转为卡片')
async def _(event: Event):
	user, repo = getUrl(event.get_plaintext())
	yield MessageSegment.image(f"https://opengraph.githubassets.com/githubcard/{user}/{repo}")
