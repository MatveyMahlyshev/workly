from fastapi import APIRouter

from .skills.controllers import router as skill_router

router = APIRouter(prefix="/recruiting")

router.include_router(
    router=skill_router,
    tags=["Skills"],
    prefix="/skills",
)
