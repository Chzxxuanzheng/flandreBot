from core import regexMatcher
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import MessageSegment
from re import search
import httpx

from .config import config

class StatusError(Exception):
	def __init__(self, code: int):
		self.code = code

	def __str__(self):
		return f"错误，状态码：{self.code}"

pattern = r"(?:https?://)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"

voidImg: bytes
basePath = __file__.rsplit('/', 1)[0]
with open(f'{basePath}/void.png', 'rb') as f:
	voidImg = f.read()

def getUrl(txt: str) -> str | None:
    """获取github项目链接（只保留github.com/owner/repo）"""
    # 匹配 http(s)://github.com/owner/repo 或 github.com/owner/repo
    m = search(pattern, txt)
    if m:
        return m.group(1), m.group(2)
    return None


async def requestImg(url: str):
	"""请求图片，返回图片"""
	async with httpx.AsyncClient(proxy=config.proxy) as client:
		response = await client.get(url)
		if response.status_code == 200:
			return response.content
		else:
			raise StatusError(response.status_code)


@regexMatcher(pattern, desc='github连接转为卡片')
async def _(event: Event):
	user, repo = getUrl(event.get_plaintext())
	try:
		img = await requestImg(f"https://opengraph.githubassets.com/githubcard/{user}/{repo}")
		if img == voidImg:
			yield ['获取github卡片失败：', "该项目不存在"]
		else:
			yield MessageSegment.image(img)
	except StatusError as e:
		yield ['获取github卡片失败：', str(e)]
	except (TimeoutError, httpx.ReadTimeout) as e:
		yield ['获取github卡片失败：', "请求超时"]
	except (httpx.RemoteProtocolError):
		yield ['获取github卡片失败：', "连接失败"]
	except Exception as e:
		yield ['获取github卡片失败：', "未知错误"]
		raise e
