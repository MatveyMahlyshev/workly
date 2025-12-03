from fastapi import Depends


from users.infrastructure.repositories import SQLCandidateRepositoryImpl
from users.application.use_cases import CandidateUseCase
from users.presentation.dependencies import get_password_hasher
from shared.dependencies.db import get_db


def get_candidate_repository(session=Depends(get_db)):
    return SQLCandidateRepositoryImpl(session=session)


def get_candidate_use_cases(
    user_repo=Depends(get_candidate_repository),
    password_hasher=Depends(get_password_hasher),
):
    return CandidateUseCase(repo=user_repo, password_hasher=password_hasher)
