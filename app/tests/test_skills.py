import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_skills(client_with_skills: AsyncClient):
    """Тест получения списка навыков (уже есть 3 навыка)"""
    response = await client_with_skills.get("/api/v2/recruiting/skills/list/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


@pytest.mark.asyncio
async def test_create_skill(client_with_skills: AsyncClient):
    response = await client_with_skills.post(
        "/api/v2/recruiting/skills/create/",
        json={"title": "skill_5"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "success"}
