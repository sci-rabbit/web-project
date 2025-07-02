from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, UserRelationMixin

if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user_back_populates: str | None = "posts"

    tittle: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
