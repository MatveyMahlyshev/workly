import pytest
from httpx import AsyncClient


class TestSkills:
    @pytest.mark.asyncio
    async def test_get_skills(self, async_client: AsyncClient):
        response = await async_client.get("/api/v2/recruiting/skills/list/")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "field,value,expected",
        [
            ("title", "skill_4", 201),
            ("title", None, 422),
            ("title", "", 422),
            ("title", 4, 422),
        ],
    )
    async def test_create_skill(
        self,
        async_client: AsyncClient,
        field: str,
        value: str,
        expected: int,
    ):
        response = await async_client.post(
            "/api/v2/recruiting/skills/create/",
            json={field: value},
        )
        
        assert response.status_code == expected
        
    @pytest.mark.asyncio
    async def test_create_skill_duplicate(
        self,
        async_client: AsyncClient,
    ):
        await async_client.post(
            "/api/v2/recruiting/skills/create/",
            json={"title": "skill_1"},
        )
        response = await async_client.post(
            "/api/v2/recruiting/skills/create/",
            json={"title": "skill_1"},
        )
        
        assert response.status_code == 409