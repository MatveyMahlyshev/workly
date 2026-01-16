import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
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
    from shared.infrastructure.models import Skill, Candidate, User
    from datetime import date

    # name: str = Field(min_length=2, max_length=50)
    # surname: str = Field(min_length=2, max_length=50)
    # patronymic: str | None = Field(min_length=2, max_length=50, default=None)
    # email: EmailStr = Field(min_length=5, max_length=254)
    # phone: str = Field(min_length=10, max_length=20, default=generate_phone_number())
    # birth_date: date
    # about_candidate: str | None = None
    # location: str | None = None
    #  password: str = Field(
    #     min_length=10,
    #     max_length=50,
    #     default="Stringstri11",
    # )
    # work_experience: list[Experience] | None = None
    # education: list[Education] | None = None

    # user = User(
    #         email=entity.email,
    #         surname=entity.surname,
    #         name=entity.name,
    #         patronymic=entity.patronymic,
    #         phone=entity.phone,
    #         password_hash=entity.password_hash,
    #         is_active=entity.is_active,
    #         permission_level=PermissionLevel.CANDIDATE.value,
    #     )
    #     candidate = Candidate(
    #         birth_date=entity.birth_date,
    #         about_candidate=entity.about_candidate,
    #         location=entity.location,
    #         user=user,
    #     )
    user = User(
        name="Test_name",
        surname="Test_surname",
        patronymic="Test_patronymic",
        email="testemail@gmail.com",
        phone="71234567890",
        password_hash="$2b$12$Yb5I2f/Q1JePhVfBxJgD8ujXUgXEs8AnZszfYYWb6tKEPZoofDDY.",
        is_active=True,
        permission_level=1,
    )
    candidate = Candidate(
        birth_date=date(2003, 1, 16),
        about_candidate="Test text.",
        location="Test_location",
        user=user,
    )
    db_session.add(user)
    db_session.add(candidate)
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
