import uvicorn

from server import settings


if __name__ == '__main__':
    uvicorn.run(
        'server.main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.RELOAD,
    )
