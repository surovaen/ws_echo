from fastapi import FastAPI

from routers.api.urls import router as api_router
from routers.api.v1.channels import router as ws_router
from server import settings


title = 'WebSockets'

app = FastAPI(debug=settings.DEBUG, title=title)
app.include_router(api_router, prefix='/api', tags=['api'])
app.include_router(ws_router)
