from fastapi.testclient import TestClient
from tests.confest import client
import pytest


class TestUserHr:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        self.user_data = {
            "good_email": "hr@example.com",
            "bad_email": "invalid-email",
            "good_password": "SecurePassHr123",
            "bad_password": "weak",
        }
        self.registered_users = []
        yield
        self.registered_users.clear()

    def cleanup_user(self, client: TestClient, access_token: str):
        client.delete(
            "/api/v1/users/delete/me/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    def create_valid_user(self, client: TestClient, response: bool = False):
        result = client.post(
            "/api/v1/users/register/hr/",
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
        assert response.json().get("email")
        assert response.json().get("id")

    def test_create_hr_user_failed(self, client: TestClient):
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

    def test_create_hr_user_with_bad_password(self, client: TestClient):
        response = client.post(
            "/api/v1/users/register/hr/",
            json={
                "email": self.user_data["good_email"],
                "password": self.user_data["bad_password"],
            },
        )

        assert response.status_code == 422

    def test_create_hr_user_with_bad_email(self, client: TestClient):
        response = client.post(
            "/api/v1/users/register/hr/",
            json={
                "email": self.user_data["bad_email"],
                "password": self.user_data["good_password"],
            },
        )
        assert response.status_code == 422

    def test_create_hr_user_with_no_email(self, client: TestClient):
        response = client.post(
            "/api/v1/users/register/hr/",
            json={
                "password": self.user_data["good_password"],
            },
        )
        assert response.status_code == 422

    def test_create_hr_user_with_no_password(self, client: TestClient):
        response = client.post(
            "/api/v1/users/register/hr/",
            json={
                "email": self.user_data["good_email"],
            },
        )
        assert response.status_code == 422

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

        assert response.json().get("access_token")
        assert response.json().get("refresh_token")
        assert response.json().get("token_type") == "bearer"

    def test_login_hr_user_not_found(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/login/",
            data={
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        assert response.status_code == 404

    def test_login_hr_user_bad_email(self, client: TestClient):
        self.create_valid_user(client=client, response=False)
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

        response = client.post(
            "/api/v1/auth/login/",
            data={
                "email": self.user_data["bad_email"],
                "password": self.user_data["good_password"],
            },
        )
        self.cleanup_user(
            client=client,
            access_token=access_token,
        )

        assert response.status_code == 422
        assert response.json().get("detail")
