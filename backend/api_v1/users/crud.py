from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from auth.auth_helpers import get_user_by_token_sub
from auth.utils import hash_password
from .schemas import CreateUserWithProfile, UserCreate
from core.models import User, CandidateProfile
import exceptions


async def create_user(session: AsyncSession, user: dict | UserCreate):
    email_exists = await session.execute(
        select(User.email).where(User.email == user["email"])
    )
    if email_exists.scalar_one_or_none():
        raise exceptions.ConflictException.EMAIL_ALREADY_EXISTS
    if isinstance(user, UserCreate):
        permission_level = 2
    else:
        permission_level = 1
    new_user = User(
        email=user["email"],
        password_hash=hash_password(user["password"]),
        is_active=True,
        permission_level=permission_level,
    )

    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Integrity error.",
        )

    return {
        "id": new_user.id,
        "email": new_user.email,
    }


async def create_user_with_profile(
    session: AsyncSession, user_profile: CreateUserWithProfile
) -> dict:
    user: dict = await create_user(
        session=session,
        user={
            "email": user_profile.email,
            "password": user_profile.password,
        },
    )

    profile = CandidateProfile(
        name=user_profile.name.lower().capitalize(),
        surname=user_profile.surname.lower().capitalize(),
        patronymic=user_profile.patronymic.lower().capitalize(),
        about_candidate=user_profile.about_candidate,
        education=user_profile.education,
        birth_date=user_profile.birth_date,
        work_experience=user_profile.work_experience,
        user_id=user.get("id"),
    )
    session.add(profile)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Integrity error.",
        )

    return profile


async def delete_user(
    payload: dict,
    session: AsyncSession,
):
    user = await get_user_by_token_sub(
        payload=payload,
        session=session,
    )
    await session.delete(user)
    await session.commit()
