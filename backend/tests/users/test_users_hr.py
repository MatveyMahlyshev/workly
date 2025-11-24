from fastapi.testclient import TestClient
from tests.confest import client
import pytest
from .setup_data import SetupData


class TestUserHr(SetupData):
    def create_valid_user(self, client: TestClient, response: bool = False):
        result = client.post(
            "/api/v1/users/register/",
            json={
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        if response:
            return result

    def test_create_hr_user_success(self, client: TestClient):
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

    def test_create_hr_user_exists_409(self, client: TestClient):
        self.create_valid_user(client=client, response=False)
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

        assert response.status_code == 409
        assert response.json().get("detail")

    @pytest.mark.parametrize(
        "invalid_data, value",
        [
            ("password", "badpassword"),
            ("password", None),
            ("email", "bademail"),
            ("email", None),
        ],
    )
    def test_create_hr_unproccessable_422(
        self,
        client: TestClient,
        invalid_data,
        value,
    ):
        if value is None:
            self.hr_user_data.pop(invalid_data)
        else:
            self.hr_user_data[invalid_data] = value
        response = client.post("/api/v1/users/register/", json=self.candidate_user_data)

        assert response.status_code == 422
        assert response.json().get("detail")

    def test_login_hr_user_success(self, client: TestClient):
        self.create_valid_user(client=client, response=False)
        response = client.post(
            "/api/v1/auth/login/",
            data={
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        self.cleanup_user(
            client=client,
            access_token=response.json().get("access_token"),
        )

        assert response.status_code == 200
        assert response.json().get("access_token")
        assert response.json().get("refresh_token")
        assert response.json().get("token_type") == "bearer"

    def test_login_hr_user_not_found_404(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/login/",
            data={
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        assert response.status_code == 404
