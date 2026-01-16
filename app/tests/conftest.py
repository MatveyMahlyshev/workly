import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport  # Добавлен ASGITransport!
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text

from main import app
from shared.infrastructure.base import Base
from shared.dependencies.db import get_db
from shared.config.settings import settings


@pytest.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        settings.db.test_url,
        echo=False,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
def session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session


@pytest.fixture
async def setup_data(db_session: AsyncSession):
    from shared.infrastructure.models import Skill

    skills_data = [{"title": "skill_1"}, {"title": "skill_2"}, {"title": "skill_3"}]
    created_skills = []

    for skill_data in skills_data:
        skill = Skill(**skill_data)
        db_session.add(skill)
        created_skills.append(skill)

    await db_session.commit()
    return [skill.id for skill in created_skills]


@pytest.fixture
async def client(session_factory):

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(client: AsyncClient, setup_data):
    client.skill_ids = setup_data
    yield client
