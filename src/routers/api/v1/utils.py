from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.encoders import jsonable_encoder
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from db.repository import HistoryRepository, UserRepository
from db.user import User
from models.history import HistoryModel
from server import settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Функция верификации пароля пользователя."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Функция получения зашифрованного пароля."""
    return pwd_context.hash(password)


async def authenticate_user(
        session: AsyncSession,
        username: str,
        password: str,
) -> Optional[User]:
    """Функция аутентификации пользователя."""
    user = await UserRepository.get(session=session, username=username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Функция создания jwt access-токена."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update(
        {
            'exp': expire,
        },
    )

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def validate_user_token(token: str, session: AsyncSession) -> Optional[User]:
    """Функция валидации jwt access-токена и получение пользователя."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await UserRepository.get(session=session, username=username)

    if user is None:
        raise credentials_exception

    return user


async def validate_ws_user(session: AsyncSession, username: str):
    """Функция валидации пользователя вебсокета."""
    message = 'Не удалось проверить учетные данные'
    user = await UserRepository.get(session=session, username=username)
    if user is None:
        return False, message
    try:
        payload = jwt.decode(user.token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # noqa F841
    except JWTError:
        return False, message

    return user, None


def create_ws_link(username: str, ws_type: str) -> str:
    """Функция формирования ссылки на вебсокет."""
    ws_link = f'ws://{settings.APP_HOST}:{settings.APP_PORT}/{ws_type}/{username}'
    return ws_link


async def update_history(session: AsyncSession, username: str, ws_history: HistoryModel):
    """Функция обновления истории переписки пользователя."""
    user_history = await HistoryRepository.get_or_create(session=session, username=username)
    user_history = user_history.api_model
    user_history.records.extend(ws_history.records)

    await HistoryRepository.update(
        session=session,
        username=username,
        records=jsonable_encoder(
            user_history.model_dump().get('records', []),
        ),
    )
