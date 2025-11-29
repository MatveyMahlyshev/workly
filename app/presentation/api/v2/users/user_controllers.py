from fastapi import APIRouter, Depends

from application.use_cases.user import UserUseCase
from presentation.schemas import UserCreate, SuccessResponse
from .dependencies import get_user_use_cases

router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/register/", response_model=SuccessResponse)
async def create_user(
    user_data: UserCreate, use_cases: UserUseCase = Depends(get_user_use_cases)
):
    return await use_cases.create_user(
        surname=user_data.surname,
        name=user_data.name,
        patronymic=user_data.patronymic,
        email=user_data.email,
        password=user_data.password,
    )
