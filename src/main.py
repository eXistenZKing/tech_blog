from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import UserRole
from src.auth.config import auth_backend, fastapi_users
from src.auth.schemas import UserCreate, UserRead, UserUpdate
from .database import get_async_session
# from src.posts.routes import router as posts_router


app = FastAPI(
    title="Technical Blog"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Register"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

# app.include_router(posts_router)


# async def add_role(name: str, session: AsyncSession = Depends(get_async_session)):
#     # Создаём объект User (инстанс модели)
#     admin_role = UserRole(name=name)
#     # Добавляем объект в сессию
#     session.add(admin_role)
#     # Сохраняем изменения в базе данных
#     await session.commit()


# add_role("Администратор")
