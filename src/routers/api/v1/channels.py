import datetime

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect
import websockets

from core.sockets import WSManager
from models.enums import SourceType
from models.history import HistoryModel, RecordModel
from routers.api.v1.utils import update_history, validate_ws_user
from server import settings
from server.database import get_session


router = APIRouter()
ws_manager = WSManager()


@router.websocket('/echo_ws/{username}')
async def echo_websocket(
        websocket: WebSocket,
        username: str,
        session: AsyncSession = Depends(get_session),
):
    """Обработка передачи данных в эхо-канале с учетом прокси."""
    user, message = await validate_ws_user(session, username)

    if not user:
        await websocket.accept()
        return await websocket.send_text(message)

    await websocket.accept()
    ws_history = HistoryModel()

    try:
        while True:
            data = await websocket.receive_text()
            client_record = RecordModel(
                time=datetime.datetime.now(),
                source=SourceType.ECHO_CLIENT.value,
                message=data,
            )

            if settings.IS_PROXY:
                async with websockets.connect(settings.FAKE_ECHO_SERVER) as ws:
                    req_data = await ws.recv()  # noqa F841
                    await ws.send(data)
                    data = await ws.recv()

            await websocket.send_text(data)

            server_record = RecordModel(
                time=datetime.datetime.now(),
                source=SourceType.SERVER.value,
                message=data,
            )
            ws_history.records.extend([client_record, server_record])

    except WebSocketDisconnect:
        await update_history(session, username, ws_history)


@router.websocket('/pub_ws/{username}')
async def public_websocket(
        websocket: WebSocket,
        username: str,
        session: AsyncSession = Depends(get_session),
):
    """Обработка передачи данных в публичном канале."""
    user, message = await validate_ws_user(session, username)

    if not user:
        await websocket.accept()
        return await websocket.send_text(message)

    await ws_manager.connect(websocket, username)
    welcome_message = f'Приветствую в чате, {username}!'
    await websocket.send_text(welcome_message)

    for message in ws_manager.messages:
        await websocket.send_text(message)

    try:
        while True:
            data = await websocket.receive_text()
            message = f'{username}: {data}'
            ws_manager.add_message(message)
            await ws_manager.send_message(message)
    except WebSocketDisconnect:
        await ws_manager.disconnect(websocket, username)
