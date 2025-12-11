from fastapi import APIRouter

from .skills.controllers import router as skill_router
from .vacancies.controllers import router as vacancy_router
from .questions.controllers import router as questions_router

router = APIRouter(prefix="/recruiting")

router.include_router(
    router=skill_router,
    tags=["Skills"],
    prefix="/skills",
)

router.include_router(
    router=vacancy_router,
    tags=["Vacancies"],
    prefix="/vacancies",
)

router.include_router(
    router=questions_router,
    tags=["Questions"],
    prefix="/questions",
)
