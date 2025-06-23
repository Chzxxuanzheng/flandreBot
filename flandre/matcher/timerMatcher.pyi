from ._matcherCommonImport import *
from datetime import date

@overload
def cronMatcher(
	*,
	second: Optional[int|str]=...,
	minute: Optional[int|str]=...,
	hour: Optional[int|str]=...,
	day: Optional[int|str]=...,
	day_of_week: Optional[int|str]=...,
	week: Optional[int|str]=...,
	month: Optional[int|str]=...,
	year: Optional[int|str]=...,
	start_date: Optional[date|datetime|str]=...,
	end_date: Optional[date|datetime|str]=...,
    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]:...
@overload
def cronMatcher(
	*,
	second: Optional[int|str]=...,
	minute: Optional[int|str]=...,
	hour: Optional[int|str]=...,
	day: Optional[int|str]=...,
	day_of_week: Optional[int|str]=...,
	week: Optional[int|str]=...,
	month: Optional[int|str]=...,
	year: Optional[int|str]=...,
	start_date: Optional[date|datetime|str]=...,
	end_date: Optional[date|datetime|str]=...,

	defaultTarget: Target,

    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]: ...
@overload
def cronMatcher(
	*,
	second: Optional[int|str]=...,
	minute: Optional[int|str]=...,
	hour: Optional[int|str]=...,
	day: Optional[int|str]=...,
	day_of_week: Optional[int|str]=...,
	week: Optional[int|str]=...,
	month: Optional[int|str]=...,
	year: Optional[int|str]=...,
	start_date: Optional[date|datetime|str]=...,
	end_date: Optional[date|datetime|str]=...,

    msgType: Optional[Literal['group', 'private']],
    id: int | str,
    platform: Optional[ScopeLiteral | SupportScope]=...,
	
    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]: ...

from ._matcherCommonImport import *

@overload
def intervalMatcher(
	*,
	seconds: Optional[int]=...,
	minutes: Optional[int]=...,
	hours: Optional[int]=...,
	days: Optional[int]=...,
	months: Optional[int]=...,
	years: Optional[int]=...,
	start_date: Optional[date|datetime]=...,
	end_date: Optional[date|datetime]=...,
    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]:...
@overload
def intervalMatcher(
	*,
	seconds: Optional[int]=...,
	minutes: Optional[int]=...,
	hours: Optional[int]=...,
	days: Optional[int]=...,
	months: Optional[int]=...,
	years: Optional[int]=...,
	start_date: Optional[date|datetime]=...,
	end_date: Optional[date|datetime]=...,

	defaultTarget: Target,

    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]: ...
@overload
def intervalMatcher(
	*,
	seconds: Optional[int]=...,
	minutes: Optional[int]=...,
	hours: Optional[int]=...,
	days: Optional[int]=...,
	months: Optional[int]=...,
	years: Optional[int]=...,
	start_date: Optional[date|datetime]=...,
	end_date: Optional[date|datetime]=...,

    msgType: Optional[Literal['group', 'private']],
    id: int | str,
    platform: Optional[ScopeLiteral | SupportScope]=...,
	
    # Matcher 通用参数
    desc: str,
    rule: Optional[Rule | T_RuleChecker]=...,
    permission: Optional[Permission | T_PermissionChecker]=...,
    handlers: Optional[list[T_Handler | Dependent[Any]]]=...,
    temp: Optional[bool]=...,
    expire_time: Optional[datetime | timedelta]=...,
    priority: Optional[int]=...,
    block: Optional[bool]=...,
    state: Optional[T_State]=...,
) -> Callable[[Any],T_Handler]: ...