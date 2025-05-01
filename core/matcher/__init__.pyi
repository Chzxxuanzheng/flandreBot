from datetime import datetime, timedelta, date
from typing import Any, Callable, Literal, Optional

from nonebot.dependencies import Dependent
from nonebot.permission import Permission
from nonebot.rule import Rule
from nonebot.typing import T_Handler, T_PermissionChecker, T_RuleChecker, T_State
from nonebot.adapters import Message, MessageSegment

# 结束当前处理，发送消息并停止后续的处理函数
def finish(
	msg: str|Message|MessageSegment|list[MessageSegment]
)-> None:...
# 定义一个命令响应器，用于匹配特定命令并执行相应的处理函数
def commandMatcher(
 	*name: list[str],
	desc: str,
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent[Any]] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> Callable[[Any],T_Handler]: ...
# 定义一个消息响应器，用于匹配特定规则的消息并执行相应的处理函数
def messageMatcher(
	desc: str,
    rule: Rule | T_RuleChecker | None = ...,
    permission: Permission | T_PermissionChecker | None = ...,
    handlers: list[T_Handler | Dependent[Any]] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    priority: int = ...,
    block: bool = ...,
    state: T_State | None = ...,
) -> Callable[[Any],T_Handler]: ...
# 定义一个驱动器连接响应器，用于在特定的消息类型和ID下执行相应的处理函数
def connectMatcher(
	*,
	msgType: Literal['group','private'],
	id: int, 
	desc: str,
    rule: Rule | T_RuleChecker | None = None,
	handlers: list[T_Handler | Dependent[Any]] | None = ...,
	priority: int = ...,
	state: T_State | None = ...,
) -> Callable[[Any],T_Handler]:...
# def timerMatcher(
# 	msgType: Literal['group','private'],
# 	id: int,
# 	trigger: Literal['cron','interval'],
# 	*,
# 	second: Optional[int] = ...,
# 	minute: Optional[int] = ...,
# 	hour: Optional[int] = ...,
# 	day: Optional[int] = ...,
# 	month: Optional[int] = ...,
# 	year: Optional[int] = ...,
# 	desc: str,
#     rule: Rule | T_RuleChecker | None = ...,
#     handlers: list[T_Handler | Dependent[Any]] | None = ...,
#     temp: bool = ...,
#     expire_time: datetime | timedelta | None = ...,
#     state: T_State | None = ...,
# ) -> Callable[[Any],T_Handler]: ...
def cronMatcher(
	msgType: Literal['group','private'],
	id: int,
	*,

	second: Optional[int|str] = ...,
	minute: Optional[int|str] = ...,
	hour: Optional[int|str] = ...,
	day: Optional[int|str] = ...,
	day_of_week: Optional[int|str] = ...,
	week: Optional[int|str] = ...,
	month: Optional[int|str] = ...,
	year: Optional[int|str] = ...,
	start_date: Optional[date|datetime|str] = ...,
	end_date: Optional[date|datetime|str] = ...,

	desc: str,
    rule: Rule | T_RuleChecker | None = ...,
    handlers: list[T_Handler | Dependent[Any]] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    state: T_State | None = ...,
) -> Callable[[Any],T_Handler]: ...
def intervalMatcher(
	msgType: Literal['group','private'],
	id: int,
	*,

	seconds: Optional[int] = ...,
	minutes: Optional[int] = ...,
	hours: Optional[int] = ...,
	days: Optional[int] = ...,
	months: Optional[int] = ...,
	years: Optional[int] = ...,
	start_date: Optional[date|datetime] = ...,
	end_date: Optional[date|datetime] = ...,

	desc: str,
    rule: Rule | T_RuleChecker | None = ...,
    handlers: list[T_Handler | Dependent[Any]] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    state: T_State | None = ...,
) -> Callable[[Any],T_Handler]: ...
def matcherErrorMatcher(
	msgType: Literal['group','private'],
	id: int,
	*,
	desc: str,
    rule: Rule | T_RuleChecker | None = ...,
    handlers: list[T_Handler | Dependent[Any]] | None = ...,
    temp: bool = ...,
    expire_time: datetime | timedelta | None = ...,
    state: T_State | None = ...,
) -> Callable[[Any],T_Handler]: ...