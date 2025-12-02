from fastapi import Depends


from infastructure.repositories import CandidateRepositoryImpl
from application.use_cases import CandidateUseCase
from presentation.dependencies import get_db, get_password_hasher


def get_candidate_repository(session=Depends(get_db)):
    return CandidateRepositoryImpl(session=session)


def get_candidate_use_cases(
    user_repo=Depends(get_candidate_repository),
    password_hasher=Depends(get_password_hasher),
):
    return CandidateUseCase(repo=user_repo, password_hasher=password_hasher)
