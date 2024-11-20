from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UserRole(Base):
    """Перечень ролей для модели пользователя."""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    role_name: Mapped[str] = mapped_column(
        String, ForeignKey("roles.name"), server_default="Пользователь"
    )
