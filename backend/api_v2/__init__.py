from fastapi import APIRouter

from auth.views import router as auth_router
from api_v1.users.views import router as users_router
from .profiles.views import router as profiles_router
from .skills.views import router as skills_router

router = APIRouter()

prefix = "api/v2/"
router.include_router(
    router=auth_router,
    prefix="/auth",
    tags=[f"{prefix}auth"],
)
router.include_router(
    router=users_router,
    prefix="/users",
    tags=[f"{prefix}users"],
)
router.include_router(
    router=profiles_router,
    prefix="/profile",
    tags=[f"{prefix}profile"],
)
router.include_router(
    router=skills_router,
    prefix="/skills",
    tags=[f"{prefix}skills"],
)
