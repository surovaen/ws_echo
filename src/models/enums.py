import enum


class SourceType(enum.Enum):
    """Перечисление источников сообщений."""

    ECHO_CLIENT = 'client'
    SERVER = 'server'
