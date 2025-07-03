from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from .mixin import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_nullable = False
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(44))
    last_name: Mapped[str | None] = mapped_column(String(44))
    bio: Mapped[str | None]
