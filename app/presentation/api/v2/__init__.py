from fastapi import APIRouter

from .users.user_controllers import router as users_router

router = APIRouter()

router.include_router(router=users_router)
