from fastapi import APIRouter

from api_v1.skills.views import router as skills_router
from api_v1.profiles.views import router as profile_router
from api_v1.vacancies.views import router as vacancy_router
from api_v1.skill_tests.views import router as skill_tests_router

router = APIRouter()
prefix = "api/v1/"
router.include_router(
    skills_router,
    prefix="/skills",
    tags=[f"{prefix}skills"],
)
router.include_router(
    router=profile_router,
    prefix="/profile",
    tags=[f"{prefix}profile"],
)
router.include_router(
    router=vacancy_router, prefix="/vacancies", tags=[f"{prefix}vacancies"]
)
router.include_router(
    router=skill_tests_router, prefix="/skill_test", tags=[f"{prefix}skill_tests"]
)
