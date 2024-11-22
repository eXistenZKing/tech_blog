from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_category, get_post_with_comments, get_comment
from .exceptions import NotFoundException
from src.database import get_async_session
from src.auth.models import User


async def get_post_util(
        post_id: int, session: AsyncSession = Depends(get_async_session)
):
    post = await get_post_with_comments(session, post_id=post_id)
    if not post:
        raise NotFoundException
    return post


async def get_comment_util(
        post_id: int, comment_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    comment = await get_comment(
        session=session, post_id=post_id, comment_id=comment_id
    )
    if not comment:
        raise NotFoundException
    return comment


async def get_category_util(
    categorys_slug: str, session: AsyncSession = Depends(get_async_session)
):
    category = await get_category(
        session=session, category_slug=categorys_slug
    )
    if not category:
        raise NotFoundException
    return category


# async def get_user(
#         id: int, session: AsyncSession = Depends(get_async_session)
# ):
#     user = await session.scalar(select(User).filter_by(id=id))
#     return user
