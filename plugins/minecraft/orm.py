from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column


class Admin(Model):
    qq: Mapped[str] = mapped_column(primary_key=True)
    
class Player(Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    qq: Mapped[str]
    
class ChatGroup(Model):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]