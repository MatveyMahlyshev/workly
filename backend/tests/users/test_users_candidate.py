from fastapi.testclient import TestClient
from tests.confest import client
import pytest

from tests.setup_data import SetupData


class TestUserCandidate(SetupData):

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
        response = client.post("/api/v2/users/register/", json=self.candidate_user_data)

        if response.status_code == 201:
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
            self.cleanup_user(client=client, access_token=access_token)
        assert response.status_code == 201
        assert response.json().get("message") == "success"

    @pytest.mark.parametrize(
        "field, value",
        [
            ("password", "badpassword"),
            ("password", None),
            ("email", "bademail"),
            ("email", None),
            ("name", ""),
            ("name", None),
            ("surname", ""),
            ("surname", None),
            ("birth_date", ""),
            ("birth_date", None),
        ],
    )
    def test_create_candidate_invalid_data_422(
        self,
        client: TestClient,
        field,
        value,
    ):
        if value is None:
            self.candidate_user_data.pop(field)
        else:
            self.candidate_user_data[field] = value
        response = client.post("/api/v2/users/register/", json=self.candidate_user_data)

        assert response.status_code == 422
        assert response.json().get("detail")
