from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer

from core.models import db_helper
from .schemas import CreateUserWithProfile, UserCreate, User
from . import crud
from auth.dependencies import get_current_token_payload

router = APIRouter(tags=["Users"])
auth = APIRouter(dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.post("/register/candidate/", status_code=status.HTTP_201_CREATED)
async def create_user_with_profile(
    user_profile: CreateUserWithProfile,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user_with_profile(
        session=session, user_profile=user_profile
    )


@router.post("/register/hr/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user=user)


@auth.delete("/delete/me/", status_code=status.HTTP_204_NO_CONTENT)
async def create_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.delete_user(session=session, payload=payload)


router.include_router(router=auth)
