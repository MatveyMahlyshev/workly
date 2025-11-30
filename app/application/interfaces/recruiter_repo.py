from abc import ABC, abstractmethod

from .user_repo import IUserRepository


class IRecruiterRepo(IUserRepository, ABC):
    pass
