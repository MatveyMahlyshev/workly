import pytest
from tests.confest import client
from fastapi.testclient import TestClient


class SetupData:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = {
            "good_email": "test@example.com",
            "bad_email": "invalid-email",
            "good_password": "SecurePassHr123",
            "bad_password": "weak",
        }
        self.candidate_user_data = {
            "name": "Test",
            "surname": "Test",
            "patronymic": "Test",
            "about_candidate": "Test",
            "education": "Test",
            "birth_date": "2003-05-18",
            "work_experience": "Test",
            "email": None,
            "password": None,
        }
        self.hr_user_data = {
            "email": self.user_data["good_email"],
            "password": self.user_data["good_password"],
        }

        self.registered_users = []
        yield
        self.registered_users.clear()

    def cleanup_user(self, client: TestClient, access_token: str):
        client.delete(
            "/api/v1/users/delete/me/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
