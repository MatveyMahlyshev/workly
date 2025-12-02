from fastapi import HTTPException, status

from presentation.schemas import SuccessfullResponse
from domain.exceptions import EmailAlreadyExists, PhoneAlreadyExists, CreateObjectException


async def create_user(use_cases, user_data):
    try:
        await use_cases.create_user(**user_data.model_dump())
        return SuccessfullResponse()
    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    except PhoneAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered",
        )
    except CreateObjectException:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error of creating user",
        )