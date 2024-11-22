"""
Схемы (модели pydantic) для работы с Post, Categories, Comments.
"""

from typing import Optional

from pydantic import (BaseModel,
                      Field, computed_field,
                      field_validator)
from slugify import slugify

from .exceptions import EmptyValueException


MAX_LEN_COMM_MSG = "Макс. длина комментария 500 символов."


class PostGet(BaseModel):
    id: int
    title: str
    text: str
    category: str
    author: int

    # @computed_field
    # async def comments(
    #     self,
    #     session: AsyncSession = Depends(get_async_session)
    # ) -> dict[int, Union[list, None]]:
    #     comments = await session.scalar(select(Comment)
    #                                     .where(Comment.post_id == self.id))
    #     # count = len(comments)
    #     return {"count": count,
    #             "comments": comments}


class PostListGet(BaseModel):
    id: int
    title: str
    text: str
    category: str
    author: int


class PostCreate(BaseModel):
    title: str
    text: str
    category: str

    @field_validator('title', mode="before")
    @classmethod
    def validate_title(cls, title: str):
        if len(title) == 0:
            raise EmptyValueException(detail="title")
        return title

    @field_validator('text', mode="before")
    @classmethod
    def validate_text(cls, text: str):
        if len(text) == 0:
            raise EmptyValueException(detail="text")
        return text


class PostUpdate(PostCreate):
    title: Optional[str]
    text: Optional[str]
    category: Optional[str]


class CommentGet(BaseModel):
    id: int
    author: int
    text: str
    post_id: int


class CommentCreate(BaseModel):
    text: str = Field(
        max_length=500, description=MAX_LEN_COMM_MSG)

    @field_validator('text', mode="before")
    @classmethod
    def validate_text(cls, text: str):
        if len(text) == 0:
            raise EmptyValueException(detail="text")
        return text


class CategoryGet(BaseModel):
    id: int
    name: str
    slug: str


class CategoryListGet(BaseModel):
    id: int
    name: str
    slug: str


class CategoryCreate(BaseModel):
    name: str

    @computed_field
    def slug(self) -> str:
        return slugify(self.name)
