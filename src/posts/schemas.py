from pydantic import (BaseModel,
                      Field, computed_field,
                      field_validator)
from slugify import slugify


class ErrorMessage(BaseModel):
    detail: str


class Category(BaseModel):
    id: int
    name: str
    slug: str


class CategoryCreate(BaseModel):
    name: str

    @computed_field
    def slug(self) -> str:
        return slugify(self.name)


class PostGet(BaseModel):
    id: int
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
            raise ValueError('Поле title не может быть пустым.')
        return title

    @field_validator('text', mode="before")
    @classmethod
    def validate_text(cls, text: str):
        if len(text) == 0:
            raise ValueError('Поле text не может быть пустым.')
        return text


class PostUpdate(PostCreate):
  title: Optional[str]
  text: Optional[str]
  category: Optional[str]


class Comment(BaseModel):
    id: int
    author: int
    text: str
    post_id: int


class CommentCreate(BaseModel):
    author: int
    text: str = Field(
        max_length=500, description="Макс. длина комментария 500 символов.")
    post_id: int
