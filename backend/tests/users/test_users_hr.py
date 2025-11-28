from fastapi.testclient import TestClient
from tests.confest import client
import pytest
from tests.setup_data import SetupData


class TestUserHr(SetupData):
    def test_create_hr_200(self, client: TestClient):
        response = self.create_valid_user_hr(client=client, response=True)
        access_token = (
            client.post(
                "/api/v2/auth/login/",
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
        self.create_valid_user_hr(client=client, response=False)
        response = self.create_valid_user_hr(client=client, response=True)
        access_token = (
            client.post(
                "/api/v2/auth/login/",
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
        "field, value",
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
        field,
        value,
    ):
        if value is None:
            self.hr_user_data.pop(field)
        else:
            self.hr_user_data[field] = value
        response = client.post("/api/v2/users/register/", json=self.candidate_user_data)

        assert response.status_code == 422
        assert response.json().get("detail")
