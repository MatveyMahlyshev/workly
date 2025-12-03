from fastapi import APIRouter

from .candidates.controllers import router as candidates_router
from .recruiters.controllers import router as recruiters_router

router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(
    router=candidates_router,
    tags=["Candidates"],
    prefix="/candidate",
)
router.include_router(
    router=recruiters_router,
    tags=["Recruiter"],
    prefix="/recruiter",
)
