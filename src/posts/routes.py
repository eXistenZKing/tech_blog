from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.schemas import PostOutSchema
from src.database import get_async_session
from src.posts.models import Post

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/")
async def posts_list(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Post).filter_by(is_published=True)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "detail": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Serer Error",
            "data": None,
            "detail": None
        })


@router.get("/{post_id}")
async def post_detail(
        post_id: int,
        session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Post).filter_by(id=post_id)
        result = await session.execute(query)
        if not query.scalar_one_or_none():
            raise HTTPException(status_code=404, detail={
                "status": "Not Found",
                "data": None,
                "detail": f"There is no article with ID {post_id}"
            })

        return {
            "status": "success",
            "data": result.mappings().all(),
            "detail": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "Serer Error",
            "data": None,
            "detail": None
        })
