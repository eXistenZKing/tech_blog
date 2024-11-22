"""
Маршрутизаторы для раздела Posts.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud import (get_list_post,
                    post_create, post_update, post_delete,
                    comment_create, comment_delete)
from ..exceptions import FobidenToPostException
from ..schemas import (CommentGet, PostGet, PostListGet,
                       PostCreate, PostUpdate, CommentCreate)
from ..models import Post, Comment
from ..utils import get_comment_util, get_post_util
from ..pagination import Page
from src.database import get_async_session
from src.auth.config import current_active_user
from src.auth.schemas import UserRead


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=Page[PostListGet])
async def get_posts(
    session: AsyncSession = Depends(get_async_session)
):
    return await get_list_post(session)


@router.get("/{post_id}")
async def get_post(
    post: Annotated[Post, Depends(get_post_util)]
) -> PostGet:
    return post


@router.post("/")
async def create_post(
    user: Annotated[UserRead, Depends(current_active_user)],
    data: PostCreate,
    session: AsyncSession = Depends(get_async_session),
) -> PostGet:
    return await post_create(session, author_id=user.id, data=data)


@router.patch("/{post_id}", response_model=PostGet)
async def update_post(
    post: Annotated[Post, Depends(get_post_util)],
    data: PostUpdate,
    user: Annotated[UserRead, Depends(current_active_user)],
    session: AsyncSession = Depends(get_async_session)
):
    if user.id != post.author:
        raise FobidenToPostException
    return await post_update(session, post=post, data=data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    user: Annotated[UserRead, Depends(current_active_user)],
    post: Annotated[Post, Depends(get_post_util)],
    session: AsyncSession = Depends(get_async_session),
):
    if user.id != post.author:
        raise FobidenToPostException
    await post_delete(session, post=post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{post_id}")
async def create_comment(
    user: Annotated[UserRead, Depends(current_active_user)],
    data: CommentCreate,
    post: Annotated[Post, Depends(get_post_util)],
    session: AsyncSession = Depends(get_async_session),
) -> CommentGet:
    return await comment_create(
        session, author_id=user.id, data=data, post=post
    )


@router.delete("/{post_id}/comment/{comment_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    user: Annotated[UserRead, Depends(current_active_user)],
    comment: Annotated[Comment, Depends(get_comment_util)],
    session: AsyncSession = Depends(get_async_session),
):
    if user.id != comment.author and user.role_name != "Администратор":
        raise FobidenToPostException
    await comment_delete(session, comment=comment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
