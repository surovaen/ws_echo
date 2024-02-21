from fastapi import APIRouter

from routers.api.v1.urls import router as v1_router


router = APIRouter()
router.include_router(v1_router, prefix='/v1')
