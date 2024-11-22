"""
Маршрутизаторы для раздела Categories.
"""

from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import NotEnoughRightsException
from ..pagination import Page
from ..crud import get_list_categories, category_create
from ..schemas import CategoryCreate, CategoryListGet, CategoryGet
from src.auth.schemas import UserRead
from src.auth.config import current_active_user
from src.database import get_async_session


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/")
async def get_categories(
    session: AsyncSession = Depends(get_async_session)
) -> Page[CategoryListGet]:
    return await get_list_categories(session)


# @router.get("/{category_slug}")
# async def get_category(
#         category: Annotated[Category, Depends(get_category_util)]
# ):
#     return category


@router.post("/")
async def create_category(
    data: CategoryCreate,
    user: Annotated[UserRead, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session),
) -> CategoryGet:
    if user.role_name != "Администратор":
        raise NotEnoughRightsException
    return await category_create(session, data=data)
