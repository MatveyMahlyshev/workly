from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError


from users.presentation.api import router as users_router
from auth.presentation.api import router as auth_router
from recruiting.presentation.api import router as skills_router
from shared.handlers.exception_handlers import validation_exception_handler

from shared.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    router=auth_router,
    prefix=settings.api_v2_prefix,
)

app.include_router(
    router=users_router,
    prefix=settings.api_v2_prefix,
)
app.include_router(
    router=skills_router,
    prefix=settings.api_v2_prefix,
)

app.add_exception_handler(
    ValidationError,
    validation_exception_handler,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://192.168.0.7:8080",
    ],  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {
        "message": "index",
    }


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
