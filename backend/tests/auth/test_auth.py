from fastapi.testclient import TestClient

from tests.confest import client
from tests.setup_data import SetupData


class TestAuth(SetupData):
    def test_login_user_200(self, client: TestClient):
        self.create_valid_user_hr(client=client, response=False)
        response = client.post(
            "/api/v2/auth/login/",
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

    def test_login_user_404(self, client: TestClient):
        response = client.post(
            "/api/v2/auth/login/",
            data={
                "email": self.user_data["good_email"],
                "password": self.user_data["good_password"],
            },
        )
        assert response.status_code == 404

    def test_refresh_token_200(self, client: TestClient):
        self.create_valid_user_hr(client=client)
        payload = self.get_tokens(client=client)
        response = client.post(
            "/api/v2/auth/refresh/",
            headers={"Authorization": f"Bearer {payload.get("refresh_token")}"},
        )
        self.cleanup_user(client=client, access_token=payload.get("access_token"))

        assert response.status_code == 200
        assert response.json().get("access_token")
        assert response.json().get("token_type") == "bearer"

    def test_refresh_token_no_token_401(self, client: TestClient):
        response = client.post(
            "/api/v2/auth/refresh/",
        )

        assert response.status_code == 401
        assert response.json().get("detail") == "Not authenticated"

    def test_refresh_token_invalid_token_401(self, client: TestClient):
        self.create_valid_user_candidate(client=client)
        payload = self.get_tokens(client=client)
        response = client.post(
            "/api/v2/auth/refresh/",
            headers={"Authorization": f"Bearer {payload.get("refresh_token") + "invalid"}"}
        )
        self.cleanup_user(client=client, access_token=payload.get("access_token"))

        assert response.status_code == 401
        assert response.json().get("detail") == "Invalid token."

    def test_refresh_token_no_token_401(self, client: TestClient):
        response = client.post(
            "/api/v2/auth/refresh/",
        )

        assert response.status_code == 401
        assert response.json().get("detail") == "Not authenticated"
