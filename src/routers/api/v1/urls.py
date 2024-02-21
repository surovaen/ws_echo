from fastapi import APIRouter

from routers.api.v1.common import router as user_router


router = APIRouter()
router.include_router(user_router)
