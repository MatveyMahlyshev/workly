from fastapi import APIRouter

from .user_controllers import router as users_router

router = APIRouter()

router.include_router(router=users_router)
