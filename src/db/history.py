from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON

from models.history import HistoryModel
from server.database import Base


class History(Base):
    """Модель БД History."""

    __tablename__ = 'history'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    username = Column(
        String,
        nullable=False,
        unique=True,
    )
    records = Column(JSON, nullable=True)

    @property
    def api_model(self):
        """Возвращает в виде объекта json из БД."""
        return HistoryModel(records=self.records)
