# tests/conftest.py
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def clean_tables(session: AsyncSession):
    """Очищает все таблицы в правильном порядке с учетом foreign keys"""
    tables_clean_order = [
        "candidate_profile_skill_associations",
        "vacancy_skill_associations",  
        "vacancy_response_tests",
        "vacancy_responses",
        "skill_tests",
        "candidate_profiles",
        "vacancies",
        "skills",
        "users"
    ]
    
    await session.execute(text("SET CONSTRAINTS ALL DEFERRED"))
    
    for table in tables_clean_order:
        await session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
    
    await session.commit()
    yield