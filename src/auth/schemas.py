from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    role_name: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str
