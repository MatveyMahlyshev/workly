import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_skills_with_precreated_data(client_with_skills: AsyncClient):
    """Тест получения списка навыков (уже есть 3 навыка)"""
    response = await client_with_skills.get("/api/v2/recruiting/skills/list/")
    print(response)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
