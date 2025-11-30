from fastapi import Depends


from infastructure.repositories import RecruiterRepositoryImpl
from application.use_cases import RecruiterUseCase
from presentation.dependencies import get_db


async def get_recruiter_repository(session=Depends(get_db)):
    return RecruiterRepositoryImpl(session=session)


async def get_recruiter_use_cases(user_repo=Depends(get_recruiter_repository)):
    return RecruiterUseCase(repo=user_repo)
