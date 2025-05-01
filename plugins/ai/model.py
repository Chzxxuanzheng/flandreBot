from pydantic import BaseModel
from typing import Sequence


class ChoiceDelta(BaseModel):
	role: str|None = None
	content: str|None = None
class AiDataChoice(BaseModel):
	index: int
	delta: ChoiceDelta
	finish_reason: str|None = None
	logprobs: str|None = None
class PromptTokensDetails(BaseModel):
	cached_tokens: int
	text_tokens: int
	audio_tokens: int
	image_tokens: int
class CompletionTokensDetails(BaseModel):
	text_tokens: int
	audio_tokens: int
class AiDataUsage(BaseModel):
	prompt_tokens: int
	completion_tokens: int
	total_tokens: int
	prompt_tokens_details: PromptTokensDetails
	completion_tokens_details: CompletionTokensDetails
class AiData(BaseModel):
	id: str
	object: str
	created: int
	model: str
	system_fingerprint: str|None = None
	choices: list[AiDataChoice]
	usage: None|AiDataUsage = None	# token用量


# AI聊天内容
class AiContent(BaseModel):
	role: str
	content: str
# AI聊天内容列表
class AiMessage(BaseModel):
	content: list[AiContent]

	def __init__(self, data: Sequence['ChatData']): # type: ignore
		context = []
		for i in data:
			context.append(AiContent(role=i.role, content=i.content))
		context.reverse()
		super().__init__(content=context)

	def append(self, content: AiContent):
		self.content.append(content)

	def model_dump(self):
		return super().model_dump()['content']
	
class OrmContent(BaseModel):
	"""ORM内容"""
	role: str
	content: str
	user: str|None = None