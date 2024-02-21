from sqlalchemy import Column, Integer, String

from server.database import Base


class User(Base):
    """Модель БД User."""

    __tablename__ = 'user'

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
    password = Column(
        String,
        nullable=False,
    )
    token = Column(
        String,
        nullable=True,
    )
