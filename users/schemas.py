from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import EmailStr, BaseModel


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(16)]
    email: EmailStr