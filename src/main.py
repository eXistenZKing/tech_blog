from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserRole
from src.auth.config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from .database import get_async_session, async_sessionmaker
from src.posts.routers import router as posts_router


app = FastAPI(
    title="Technical Blog"
)
add_pagination(app)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(posts_router)
