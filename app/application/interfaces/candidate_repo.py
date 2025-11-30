from abc import ABC, abstractmethod

from domain.entities import CandidateEntity
from .user_repo import IUserRepository


class ICandidateRepository(IUserRepository, ABC):
    pass
