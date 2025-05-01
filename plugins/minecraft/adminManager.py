from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot import logger
from nonebot_plugin_orm import get_session, async_scoped_session
from sqlalchemy import select

from core import commandMatcher, finish

from util.api import getGroupMemberList

from .orm import Admin
from .permissionCheck import checkAdmin

@commandMatcher('op', desc='添加管理员')
async def adminAddMain(event: GroupMessageEvent):
    # 处理添加管理员的逻辑
    mid = event.message_id
    msgs = event.message
    re = ''
    uids: dict[str|str] = {}
    session = get_session()

    await checkAdmin(event)

    for msg in msgs:
        if msg.type == 'at':
            uid = msg.data['qq']
            if uid == 'all':
                continue
            uids[uid] = msg.data.get('name', '未知人士')

    if len(uids) == 0:
        finish([MessageSegment.reply(mid), '未找到被@的成员，请查看`mc帮助`'])
    
    newOp = []
    alreadyOp = []

    async with session.begin():
        for uid in uids.keys():
            if await session.get(Admin, uid):
                alreadyOp.append(uid)
            else:
                session.add(Admin(qq=uid))
                newOp.append(uid)

    if len(newOp) == 0:
        finish([MessageSegment.reply(mid), '以上用户已经全都是OP'])

    logger.info(f'新OP:{newOp}，操作者:{event.user_id}')

    re += '将以下用户设置为OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in newOp])
    if alreadyOp:
        re += '\n以下用户已经是OP了:\n' + '\n'.join([f'{uids[i]}({i})' for i in alreadyOp])

    finish([MessageSegment.reply(mid), re])


@commandMatcher('deop', desc='移除管理员')
async def adminRemoveMain(event: GroupMessageEvent):
    # 处理移除管理员的逻辑
    mid = event.message_id
    msgs = event.message
    re = ''
    uids: dict[str|str] = {}
    session = get_session()

    await checkAdmin(event)

    for msg in msgs:
        if msg.type == 'at':
            uid = msg.data['qq']
            if uid == 'all':
                continue
            uids[uid] = msg.data.get('name', '未知人士')

    if len(uids) == 0:
        finish([MessageSegment.reply(mid), '未找到被@的成员，请查看`mc帮助`'])
    
    rmOp = []
    noOp = []

    async with session.begin():
        for uid in uids.keys():
            if admin := await session.get(Admin, uid):
                await session.delete(admin)
                rmOp.append(uid)
            else:
                noOp.append(uid)

    if len(rmOp) == 0:
        finish([MessageSegment.reply(mid), '以上用户均不是OP'])

    logger.info(f'移除OP:{rmOp}，操作者:{event.user_id}')

    re += '以下用户不再是OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in rmOp])
    if noOp:
        re += '\n以下用户原本就不是OP:\n' + '\n'.join([f'{uids[i]}({i})' for i in noOp])

    finish([MessageSegment.reply(mid), re])


@commandMatcher('lsop', desc='查看管理员')
async def adminListMain(event: GroupMessageEvent, session: async_scoped_session):
    # 查看当前群组的管理员列表
    users: dict[str|str] = {str(i['user_id']):i['card'] if i['card'] else i['nickname'] for i in await getGroupMemberList(event.group_id)}
    uids = (await session.scalars(select(Admin))).all()
    msgs = []
    for i in uids:
        logger.info(f'{users.get(i.qq,"不在群内")}({i.qq})')
        msgs.append(f'{users.get(i.qq,"不在群内")}({i.qq})')
    re = '以下用户为OP用户:\n' + '\n'.join(msgs)
    finish([MessageSegment.reply(event.message_id), re])