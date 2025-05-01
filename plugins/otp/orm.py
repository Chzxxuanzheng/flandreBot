from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column
from pyotp import TOTP

class OtpKey(Model):
	name: Mapped[str] = mapped_column(primary_key=True)
	key: Mapped[str] = mapped_column(nullable=False)

	@property
	def otp(self)->TOTP:
		return TOTP(self.key)