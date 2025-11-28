from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

# from api_v1 import router as api_v1_router
# from api_v2 import router as api_v2_router
# from core.config import settings
# from exception_handlers import validation_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


# app.include_router(
#     router=api_v1_router,
#     prefix=settings.api_v1_prefix,
# )
# app.include_router(
#     router=api_v2_router,
#     prefix=settings.api_v2_prefix,
# )

# app.add_exception_handler(ValidationError, validation_exception_handler)
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