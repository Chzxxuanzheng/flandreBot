from pydantic import BaseModel

class Config(BaseModel):
	"""Plugin Config Here"""
	isProd: bool