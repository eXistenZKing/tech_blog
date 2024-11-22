from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import CategoryDoesNotExistException
from .schemas import PostCreate, PostUpdate, CommentCreate
from .models import Post, Category, Comment


async def get_category(session: AsyncSession, category_slug):
    return await session.scalar(select(Category).filter_by(slug=category_slug))


async def get_list_post(session: AsyncSession):
    return await paginate(session, select(Post))


async def get_post_with_comments(session: AsyncSession, post_id):
    return await session.scalar(
        select(Post).outerjoin(Comment).where(Post.id == post_id)
    )


async def create_post(session: AsyncSession, author_id: int, data: PostCreate):
    if data.category and not await get_category(session,
                                                category_slug=data.category):
        raise CategoryDoesNotExistException

    db_post = Post(
        **data.model_dump(),
        author=author_id,
    )
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


async def update_post(session: AsyncSession, post: Post, data: PostUpdate):
    if data.category and not get_category(session,
                                          category_slug=data.category):
        raise CategoryDoesNotExistException

    update_data = data.model_dump(exclude_unset=True)
    if 'category' in update_data:
        update_data['category_slug'] = update_data.pop('category')

    for field, value in update_data.items():
        setattr(post, field, value)

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


def delete_post(post: Post, session: AsyncSession):
    session.delete(post)
    session.commit()


def get_comment(comment_id: int, post: Post, session: AsyncSession):
    return session.scalar(
        select(Comment).where(
            Comment.id == comment_id, Comment.post_id == post.id
        )
    )


async def get_comments_of_post(post_id: Post, session: AsyncSession):
    return await session.scalar(
        select(Comment).where(Comment.post_id == post_id)
    )


def create_comment(
    data: CommentCreate, post: Post, author_id: int, session: AsyncSession
):
    comment = Comment(
        **data.model_dump(), post_id=post.id, author=author_id
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


def delete_comment(comment: Comment, session: AsyncSession):
    session.delete(comment)
    session.commit()


def update_comment(
    comment: Comment, data: CommentCreate, session: AsyncSession
):
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)

    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment
