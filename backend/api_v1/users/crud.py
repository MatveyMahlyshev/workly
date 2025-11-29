from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from auth.dependencies import get_user_by_token_sub
from app.utils import hash_password
from .schemas import CreateUserWithProfile, UserCreate
from core.models import User, CandidateProfile


async def create_user(
    user: CreateUserWithProfile | UserCreate,
    session: AsyncSession,
):
    email_exists = await session.execute(
        select(User.email).where(User.email == user.email)
    )
    if email_exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email exists",
        )

    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        is_active=True,
    )
    if type(user) == UserCreate:
        new_user.permission_level = 2
        session.add(new_user)

    else:
        new_user.permission_level = 1

        session.add(new_user)
        await session.flush()

        profile = CandidateProfile(
            name=user.name.lower().capitalize(),
            surname=user.surname.lower().capitalize(),
            patronymic=user.patronymic.lower().capitalize(),
            about_candidate=user.about_candidate,
            education=user.education,
            birth_date=user.birth_date,
            work_experience=user.work_experience,
            user_id=new_user.id,
        )
        session.add(profile)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Integrity error",
        )
    return {"message": "success"}


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
