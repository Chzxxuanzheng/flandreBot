from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    @staticmethod
    def name():
        return "随机数"
    @staticmethod
    def help():
        return '''格式:
1. >rand
	- 1-6随机数
2. >rand 最大值
	- 1-最大值随机数
3. >rand 最小值 最大值
	- 1-最大值随机数

- 注:
	rand可以用rnd代替'''