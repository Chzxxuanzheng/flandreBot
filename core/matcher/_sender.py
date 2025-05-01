from typing import Any, AsyncGenerator, Callable, Iterable
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event, Bot, GroupMessageEvent, PrivateMessageEvent
from inspect import isasyncgenfunction
from core.event import EmitEvent
from core.target import TargetType

type MsgS = str|MessageSegment
type Msg = str|Message|MessageSegment|list[MsgS]
type Handler = Callable[[Any], AsyncGenerator[None|Msg,None]]
type Sender = Callable[[Handler, Any], None]

class __FinishMatcherProcess(Exception):
    # 自定义异常类，用于提前结束Matcher处理过程
    def __init__(self, msg, *args):
        super().__init__(*args)
        self.msg = msg

def finish(msg: Any)-> None:
    # 抛出自定义异常，用于提前结束Matcher处理过程
    raise __FinishMatcherProcess(msg)

async def _matcherIter(func, *args, **kwargs)-> AsyncGenerator[Any,None]:
    # 异步迭代处理函数返回的消息，处理自定义异常
    try:
        if isasyncgenfunction(func):
            async for msg in func(*args, **kwargs):
                if not msg:continue
                yield msg
        else:
            msg = await func(*args, **kwargs)
            if not msg:return
            yield msg
    except __FinishMatcherProcess as e:
        yield e.msg
        return
    
def createSender(bot: Bot, event: Event)-> Sender:
    # 根据事件类型创建对应的Sender
    if isinstance(event, EmitEvent):
        return createEmiEventSender(bot, event)
    elif isinstance(event, Event):
        return createNorEventSender(bot, event)
    else:
        raise ValueError('event类型错误')

def createEmiEventSender(bot: Bot, event: EmitEvent)-> Sender:
    # 创建用于EmitEvent的Sender
    target = event.target
    if target.type == TargetType.PRIVATE:
        return createPrivateSender(bot, target.id)
    else:
        return createGroupSender(bot, target.id)

def createNorEventSender(bot: Bot, event: Event)-> Sender:
    # 创建用于普通Event的Sender
    if isinstance(event, PrivateMessageEvent):
        return createPrivateSender(bot, event.user_id)
    else:
        return createGroupSender(bot, event.group_id)

def createPrivateSender(bot: Bot, userId: int|str|Iterable[int|str])-> Sender:
    # 创建用于发送私聊消息的Sender
    async def send(msg):
        await sendMsg(sendPrivateNormalMsg, sendPrivateForwardMsg, bot, userId, msg)
    
    async def sender(handler: Handler, *args, **kwargs)-> None:
        async for msg in _matcherIter(handler, *args, **kwargs):
            await send(msg)
    
    return sender

def createGroupSender(bot: Bot, groupId: int|str|Iterable[int|str])-> Sender:
    # 创建用于发送群聊消息的Sender
    async def send(msg):
        await sendMsg(sendGroupNormalMsg, sendGroupForwardMsg, bot, groupId, msg)
    
    async def sender(handler: Handler, *args, **kwargs)-> None:
        async for msg in _matcherIter(handler, *args, **kwargs):
            await send(msg)
    
    return sender


async def sendMsg(
        sendNorMsg: Callable[[Bot, int, Msg], None],
        sendForMsg: Callable[[Bot, int, Msg], None],
        bot: Bot,
        targetId: int|str|Iterable[int|str],
        msg: Msg)-> None:
    # 发送消息，根据消息类型选择不同的发送方法
    hasNode = False
    hasOther = False
    if type(msg) == str:
        msg = Message(msg)
    else:
        if isinstance(msg, MessageSegment):
            msg = Message(msg)
        re = []
        for seg in msg:
            if type(seg) == str:
                seg = MessageSegment.text(seg)
            if seg.type == 'node':
                if hasOther:
                    raise ValueError('Message不能同时包含`node`和其他类型的MessageSegment')
                hasNode = True
            else:
                if hasNode:
                    raise ValueError('Message不能同时包含`node`和其他类型的MessageSegment')
                hasOther = True
            re.append(seg)
        msg = Message(re)

    if type(targetId) == int or type(targetId) == str:
        targetId = [targetId]
    for id in targetId:
        if hasNode:
            await sendForMsg(bot, id, msg)
        else:
            await sendNorMsg(bot, id, msg)

async def sendGroupNormalMsg(bot: Bot, groupId: int, msg: Message)-> None:
    # 发送群聊普通消息
    await bot.send_group_msg(group_id=str(groupId), message=msg)

async def sendGroupForwardMsg(bot: Bot, groupId: int, msg: Message)-> None:
    # 发送群聊合并转发消息
    await bot.send_group_forward_msg(group_id=int(groupId), messages=msg)

async def sendPrivateNormalMsg(bot: Bot, userId: int, msg: Message)-> None:
    # 发送私聊普通消息
    await bot.send_private_msg(user_id=str(userId), message=msg)

async def sendPrivateForwardMsg(bot: Bot, userId: int, msg: Message)-> None:
    # 发送私聊合并转发消息
    await bot.send_private_forward_msg(user_id=str(userId), messages=msg)