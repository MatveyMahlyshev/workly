from fastapi.testclient import TestClient
from tests.confest import client
import pytest

from .setup_data import SetupData


class TestUserCandidate(SetupData):
    def create_valid_user(self, client: TestClient, response: bool = False):
        result = client.post(
            "/api/v1/users/register/",
            json={
                "name": "Test",
                "surname": "Test",
                "patronymic": "Test",
                "about_candidate": "Test",
                "education": "Test",
                "birth_date": "2003-05-18",
                "work_experience": "Test",
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        if response:
            return result

    def test_create_candidate_user_success(self, client: TestClient):
        response = self.create_valid_user(client=client, response=True)
        access_token = (
            client.post(
                "/api/v1/auth/login/",
                data={
                    "email": self.user_data["good_email"],
                    "password": self.user_data["good_password"],
                },
            )
            .json()
            .get("access_token")
        )

        self.cleanup_user(
            client=client,
            access_token=access_token,
        )

        assert response.status_code == 201
        assert response.json().get("message") == "success"

    @pytest.mark.parametrize(
        "optional_field,value",
        [
            ("patronymic", None),
            ("patronymic", ""),
            ("about_candidate", None),
            ("about_candidate", ""),
            ("education", None),
            ("education", ""),
            ("work_experience", None),
            ("work_experience", ""),
        ],
    )
    def test_registration_with_optional_fields(
        self,
        client: TestClient,
        optional_field,
        value,
    ):
        self.candidate_user_data["email"] = self.user_data["good_email"]
        self.candidate_user_data["password"] = self.user_data["good_password"]
        if value is None:
            self.candidate_user_data.pop(optional_field)
        else:
            self.candidate_user_data[optional_field] = value
        response = client.post("/api/v1/users/register/", json=self.candidate_user_data)

        if response.status_code == 201:
            access_token = (
                client.post(
                    "/api/v1/auth/login/",
                    data={
                        "email": self.user_data["good_email"],
                        "password": self.user_data["good_password"],
                    },
                )
                .json()
                .get("access_token")
            )
            self.cleanup_user(client=client, access_token=access_token)
        assert response.status_code == 201
        assert response.json().get("message") == "success"

    @pytest.mark.parametrize(
        "invalid_data,value",
        [
            ("email", None),
            ("email", "bademail"),
            ("password", None),
            ("password", "badpassword"),
        ],
    )
    def test_registration_with_indalid_data(
        self,
        client: TestClient,
        invalid_data,
        value,
    ):
        if value is None:
            self.candidate_user_data.pop(invalid_data)
        else:
            self.candidate_user_data[invalid_data] = value
        response = client.post("/api/v1/users/register/", json=self.candidate_user_data)

        assert response.status_code == 422
        assert response.json().get("detail")
