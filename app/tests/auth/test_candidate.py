import pytest
from httpx import AsyncClient


class TestAuth:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "email,password,status_code",
        [
            ("testemail@gmail.com", "Testpassword11", 200),
            ("notfound@email.com", "Testpassword11", 404),
            ("testemail@gmail.com", "Badpassword11", 400),
            ("", "Testpassword11", 422),
            ("testemail@gmail.com", "", 422),
        ],
    )
    async def test_ivalid_login_data(
        self,
        async_client: AsyncClient,
        email,
        password,
        status_code,
    ):
        response = await async_client.post(
            "/api/v2/auth/login/",
            data={
                "email": email,
                "password": password,
            },
        )
        assert response.status_code == status_code

        if response.status_code == 200:
            data = response.json()
            assert data.get("access_token") is not None
            assert data.get("refresh_token") is not None
            assert data.get("token_type") is not None
