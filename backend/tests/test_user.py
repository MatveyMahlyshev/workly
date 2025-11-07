from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import pytest

from core.models import db_helper_test
from users.crud import create_user

async def test_create_user(
    session: AsyncSession = Depends(db_helper_test.scoped_session_dependency),
):
    user_data = {
        "email": "user@example.com",
        "role": "hr",
        "password": "stringstri",
    }
    
    created_user = await create_user(session=session, user=user_data)

    


