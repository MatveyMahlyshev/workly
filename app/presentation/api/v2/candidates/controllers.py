from fastapi import APIRouter, Depends, status


from presentation.schemas import SuccessfullResponse


router = APIRouter(tags=["Candidates"], prefix="/candidate")


@router.post(
    "/register/",
    response_model=SuccessfullResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Successfull request"},
        status.HTTP_409_CONFLICT: {"description": "Conflict"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
    },
    summary="Register candidate",
)
async def create_candidate(
    # user_data: UserCreate, use_cases: UserUseCase = Depends(get_user_use_cases)
):
    pass
    # return await use_cases.create_user(
    #     surname=user_data.surname,
    #     name=user_data.name,
    #     patronymic=user_data.patronymic,
    #     email=user_data.email,
    #     password=user_data.password,
    # )
