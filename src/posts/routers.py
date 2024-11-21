from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import (get_category, get_list_post, get_post_with_comments,
                   create_post, update_post, delete_post,
                   get_comment, get_comments_of_post,
                   create_comment, delete_comment, update_comment)
from .exceptions import FobidenToPostException, NotFoundException
from .schemas import PostGet, PostListGet, PostCreate, PostUpdate
# from .pagination import PagePagination
from .models import Post, Category, Comment
from .utils import get_post
from src.database import get_async_session
from src.auth.config import current_active_user
from src.auth.schemas import UserRead


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
    )


@router.get("/")
async def get_list_posts(
    session: AsyncSession = Depends(get_async_session)
) -> Page[PostListGet]:
    return await get_list_post(session)


@router.get('/{post_id}')
async def read_post(
    post: Annotated[Post, Depends(get_post)]
) -> PostGet:
    return post


@router.post('/')
async def add_new_post(
    user: Annotated[UserRead, Depends(current_active_user)],
    data: PostCreate,
    session: AsyncSession = Depends(get_async_session),
) -> PostGet:
    return await create_post(session, author_id=user.id, data=data)


@router.patch('/{post_id}', response_model=PostGet)
def edit_post(
    post: Annotated[Post, Depends(get_post)],
    data: PostUpdate,
    user: Annotated[UserRead, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session)
):
    if user.id != post.author:
        raise FobidenToPostException
    return update_post(session, post=post, data=data)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(
    user: Annotated[UserRead, Depends(current_active_user)],
    post: Annotated[Post, Depends(get_post)],
    session: AsyncSession = Depends(get_async_session),
):
    if user.id != post.author:
        raise FobidenToPostException
    delete_post(session, post=post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
