from fastapi import APIRouter

from .hrs.controllers import router as hrs_router
from .candidates.controllers import router as candidate_router

router = APIRouter()

router.include_router(router=hrs_router)
router.include_router(router=candidate_router)
