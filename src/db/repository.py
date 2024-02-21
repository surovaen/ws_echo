from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from db.history import History
from db.user import User


class UserRepository(BaseRepository):
    """Класс-репозиторий модели User."""

    _model = User


class HistoryRepository(BaseRepository):
    """Класс-репозиторий модели History."""

    _model = History

    @classmethod
    async def get_or_create(cls, session: AsyncSession, username: str):
        """Создание или получение объекта из БД."""
        instance = await cls.get(session, username)
        if instance is not None:
            return instance

        instance = cls._model(username=username, records=[])
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
