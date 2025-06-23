from ._matcherCommonImport import *

@overload
def matcherErrorMatcher(
	*,
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
def matcherErrorMatcher(
	*,

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
def matcherErrorMatcher(
	*,
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