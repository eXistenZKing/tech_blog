"""
Главный файл с приложением FastAPI.
"""

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.auth.config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.posts.routers.posts import router as posts_router
from src.posts.routers.categories import router as categories_router


app = FastAPI(
    title="Technical Blog",
    # root_path="/api/v1"
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
app.include_router(categories_router)
