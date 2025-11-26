from fastapi.testclient import TestClient
from tests.confest import client
import pytest

from tests.setup_data import SetupData


class TestUserCandidate(SetupData):

    @pytest.mark.parametrize(
        "field,value",
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
    def test_create_candidate_with_fields(
        self,
        client: TestClient,
        field,
        value,
    ):
        self.candidate_user_data["email"] = self.user_data["good_email"]
        self.candidate_user_data["password"] = self.user_data["good_password"]
        if value is None:
            self.candidate_user_data.pop(field)
        else:
            self.candidate_user_data[field] = value
        response = client.post("/api/v2/users/register/", json=self.candidate_user_data)

        if response.status_code == 201:
            access_token = self.get_tokens(client=client).get("access_token")
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

    def test_get_profile_200(self, client: TestClient):
        self.candidate_user_data["email"] = self.user_data["good_email"]
        self.candidate_user_data["password"] = self.user_data["good_password"]
        client.post("/api/v2/users/register/", json=self.candidate_user_data)
        access_token: str = self.get_tokens(client=client).get("access_token")
        response = client.get(
            "/api/v2/profile/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.cleanup_user(client=client, access_token=access_token)

        assert response.status_code == 200
        assert response.json().get("name") == "Test"
        assert response.json().get("surname") == "Test"
        assert response.json().get("patronymic") == "Test"
        assert response.json().get("about_candidate") == "Test"
        assert response.json().get("education") == "Test"
        assert response.json().get("birth_date") == "2003-05-18"
        assert response.json().get("work_experience") == "Test"
        assert response.json().get("email") == "test@example.com"
        assert response.json().get("skills") == []

    @pytest.mark.parametrize(
        "header,message",
        [
            ({"Authorization": "Bearer invalid"}, "Invalid token."),
            (None, "Not authenticated"),
        ],
    )
    def test_get_profile_401(self, client: TestClient, header, message):
        if header is None:
            response = client.get("/api/v2/profile/")
        else:
            response = client.get(
                "/api/v2/profile/",
                headers=header,
            )

        assert response.status_code == 401
        assert response.json().get("detail") == message

    @pytest.mark.parametrize(
        "header,message",
        [
            ({"Authorization": "Bearer invalid"}, "Invalid token."),
            (None, "Not authenticated"),
        ],
    )
    def test_update_profile_401(self, client: TestClient, header, message):
        if header is None:
            response = client.put("/api/v2/profile/update/")
        else:
            response = client.put(
                "/api/v2/profile/update/",
                headers=header,
            )

        assert response.status_code == 401
        assert response.json().get("detail") == message
