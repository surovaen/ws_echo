from typing import List

from fastapi import WebSocket
from loguru import logger


class WSManager:
    """Менеджер вебсокетов."""

    def __init__(self):
        self._active_connections: List[dict] = []
        self._message_queue: List[str] = []

    async def connect(self, websocket: WebSocket, username: str):
        """Метод подключения вебсокета."""
        await websocket.accept()
        ws_data = {
            'username': username,
            'websocket': websocket,
        }
        self._active_connections.append(ws_data)
        logger.info('Подключен пользователь {user}'.format(user=username))

    @property
    def messages(self):
        """Проперти очереди сообщений."""
        return self._message_queue

    def add_message(self, message: str):
        """Метод добавления сообщений в очередь."""
        self._message_queue.append(message)

    async def send_message(self, message: str):
        """Метод отправки сообщений активным вебсокетам."""
        for conn in self._active_connections:
            await conn['websocket'].send_text(message)

    async def disconnect(self, websocket: WebSocket, username: str):
        """Метод отключения вебсокета."""
        ws_data = {
            'username': username,
            'websocket': websocket,
        }
        self._active_connections.remove(ws_data)
        logger.info('Отключен пользователь {user}'.format(user=username))
