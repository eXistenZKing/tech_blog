from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import CategoryDoesNotExistException
from .schemas import CategoryCreate, PostCreate, PostUpdate, CommentCreate
from .models import Post, Category, Comment


async def get_category(session: AsyncSession, category_slug):
    return await session.scalar(select(Category).filter_by(slug=category_slug))


async def get_list_post(session: AsyncSession):
    return await paginate(session, select(Post))


async def get_post_with_comments(session: AsyncSession, post_id):
    return await session.scalar(
        select(Post).outerjoin(Comment).where(Post.id == post_id)
    )


async def post_create(session: AsyncSession, author_id: int, data: PostCreate):
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


async def post_update(session: AsyncSession, post: Post, data: PostUpdate):
    if data.category and not await get_category(session,
                                                category_slug=data.category):
        raise CategoryDoesNotExistException

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(post, field, value)

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def post_delete(session: AsyncSession, post: Post):
    await session.delete(post)
    await session.commit()


def get_comment(comment_id: int, post_id: int, session: AsyncSession):
    return session.scalar(
        select(Comment).where(
            Comment.id == comment_id, Comment.post_id == post_id
        )
    )


async def get_comments_of_post(post_id: Post, session: AsyncSession):
    return await session.scalar(
        select(Comment).where(Comment.post_id == post_id)
    )


async def comment_create(
    session: AsyncSession, data: CommentCreate, post: Post, author_id: int
):
    comment = Comment(
        **data.model_dump(), post_id=post.id, author=author_id
    )
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def comment_delete(session: AsyncSession, comment: Comment):
    await session.delete(comment)
    await session.commit()


def comment_update(
    comment: Comment, data: CommentCreate, session: AsyncSession
):
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(comment, field, value)

    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


async def get_list_categories(session: AsyncSession):
    return await paginate(session, select(Category))


async def category_create(session: AsyncSession, data: CategoryCreate):
    db_category = Category(
        **data.model_dump()
    )
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category
