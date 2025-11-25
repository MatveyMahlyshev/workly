from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer

from core.models import db_helper
from .schemas import CreateUserWithProfile, UserCreate, User
from . import crud
from api_v1.schemas import SuccessResponse
from auth.dependencies import get_current_token_payload
from api_v2.dependencies import get_db

router = APIRouter()
auth = APIRouter(dependencies=[Depends(HTTPBearer(auto_error=False))])


@router.post(
    "/register/",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse,
)
async def create_user(
    user: CreateUserWithProfile | UserCreate,
    session: AsyncSession = Depends(get_db),
):
    return await crud.create_user(session=session, user=user)


@auth.delete("/delete/me/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_db),
):
    return await crud.delete_user(session=session, payload=payload)


router.include_router(router=auth)
