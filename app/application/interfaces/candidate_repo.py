from abc import ABC, abstractmethod

from domain.entities import Candidate


class ICandidateRepository:
    @abstractmethod
    async def create_user(self, candidate_profile: Candidate) -> Candidate:
        pass

    @abstractmethod
    async def delete_user(self, payload: dict) -> None:
        pass
