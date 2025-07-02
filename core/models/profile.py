from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Profile(Base):
    _user_id_nullable: bool = False
    _user_id_unique: bool = True
    _user_back_populates: str | None = "profiles"

    first_name: Mapped[str | None] = mapped_column(String(44))
    last_name: Mapped[str | None] = mapped_column(String(44))
    bio: Mapped[str | None]
