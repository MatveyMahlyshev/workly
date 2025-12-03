from abc import ABC, abstractmethod

from .user_repo import IUserRepository


class IRecruiterRepository(IUserRepository, ABC):
    pass
