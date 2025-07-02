from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Profile(Base):
    _user_id_nullable = False
    _user_id_unique = True
    _user_back_populates = "profiles"

    first_name: Mapped[str | None] = mapped_column(String(44))
    last_name: Mapped[str | None] = mapped_column(String(44))
    bio: Mapped[str | None]
