from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column
import datetime


# 单条聊天信息
class ChatData(Model):
	pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
	model: Mapped[str] = mapped_column(nullable=False)
	id: Mapped[str] = mapped_column(nullable=False)
	role: Mapped[str] = mapped_column(nullable=False)
	content: Mapped[str] = mapped_column(nullable=False)
	user: Mapped[str] = mapped_column(nullable=True)

	def __init__(self, id: str, data, model: str):
		self.model = model
		self.id = id
		self.role = data.role
		self.content = data.content
		self.user = data.user



# 聊天记录
class CharacterSetting(Model):
	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	content: Mapped[str] = mapped_column(nullable=False)
