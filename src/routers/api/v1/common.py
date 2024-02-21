from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse, Response

from db.repository import HistoryRepository, UserRepository
from models.socket import WSLinkModel
from models.user import TokenModel, UserModel
from routers.api.v1.utils import (
    authenticate_user,
    create_access_token,
    create_ws_link,
    get_password_hash,
    validate_user_token,
)
from server import settings
from server.database import get_session


router = APIRouter()
security_scheme = HTTPBearer()


@router.post(
    '/register',
    summary='Регистрация пользователя',
)
async def register_user(user: UserModel, session: AsyncSession = Depends(get_session)):
    """Эндпойнт регистрации пользователя."""
    try:
        hash_password = get_password_hash(user.password)
        user = await UserRepository.create(session=session, username=user.username, password=hash_password)
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'Пользователь с таким именем уже существует'},
        )

    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    '/login',
    summary='Авторизация пользователя',
    status_code=status.HTTP_200_OK,
)
async def login_user(user: UserModel, session: AsyncSession = Depends(get_session)) -> TokenModel:
    """Эндпойнт авторизации пользователя."""
    user = await authenticate_user(session, user.username, user.password)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    await UserRepository.update(session, user.username, token=access_token)
    return TokenModel(token=access_token)


@router.get(
    '/echo_ws',
    summary='Получение ссылки на эхо-канал',
    status_code=status.HTTP_200_OK,
)
async def get_echo_websocket(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
        session: AsyncSession = Depends(get_session),
) -> WSLinkModel:
    """Эндпойнт получения ссылки на эхо-канал."""
    user = await validate_user_token(credentials.credentials, session)
    ws_link = create_ws_link(user.username, 'echo_ws')
    return WSLinkModel(link=ws_link)


@router.get(
    '/pub_ws',
    summary='Получение ссылки на публичный канал',
    status_code=status.HTTP_200_OK,
)
async def get_public_websocket(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
        session: AsyncSession = Depends(get_session),
) -> WSLinkModel:
    """Эндпойнт получения ссылки на эхо-канал."""
    user = await validate_user_token(credentials.credentials, session)
    ws_link = create_ws_link(user.username, 'pub_ws')
    return WSLinkModel(link=ws_link)


@router.get(
    '/history',
    summary='Получение истории переписки',
)
async def get_history(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
        session: AsyncSession = Depends(get_session),
):
    """Эндпойнт получения истории переписки."""
    user = await validate_user_token(credentials.credentials, session)
    user_history = await HistoryRepository.get_or_create(session, user.username)
    history = user_history.api_model

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(history.model_dump().get('records', [])),
    )
