import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(abc.ABC):
    """Абстрактный класс репозитория."""

    _model = None

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """Метод создания объекта в БД."""
        instance = cls._model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def get(cls, session: AsyncSession, username: str):
        """Получение одного объекта."""
        query = select(cls._model).where(cls._model.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update(cls, session: AsyncSession, username: str, **kwargs):
        """Обновление экземпляра БД."""
        instance = await cls.get(session, username)

        for key, value in kwargs.items():
            setattr(instance, key, value)

        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance
