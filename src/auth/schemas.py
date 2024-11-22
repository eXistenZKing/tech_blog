"""
Схемы (модели pydantic) для работы с пользователями.
"""

from fastapi_users import schemas
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    role_name: str
    is_active: bool = Field(exclude=True, default=True)
    is_superuser: bool = Field(exclude=True, default=False)
    is_verified: bool = Field(exclude=True, default=False)


class UserCreate(schemas.CreateUpdateDictModel):
    username: str = Field(
        min_length=2, max_length=20,
        description="Username должен быть от 2 до 20 символов"
    )
    email: EmailStr
    password: str = Field(
        min_length=6,
        description="Мин. длина пароля 6 символов."
    )


class UserUpdate(schemas.CreateUpdateDictModel):
    username: str = Field(
        min_length=2, max_length=20,
        description="Username должен быть от 2 до 20 символов"
    )
    email: EmailStr
    password: str = Field(
        min_length=6,
        description="Мин. длина пароля 6 символов."
    )
