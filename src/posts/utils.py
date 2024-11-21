from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Post
from .crud import get_comments_of_post, get_post_with_comments
from .exceptions import NotFoundException
from src.database import get_async_session


async def get_post(
        post_id: int, session: AsyncSession = Depends(get_async_session)
):
    post = await get_post_with_comments(session, post_id=post_id)
    if not post:
        raise NotFoundException
    return post
