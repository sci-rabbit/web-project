from typing import Annotated

from fastapi import APIRouter, Depends

from users.schemas import CreateUser
from users import dal

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create_user/")
def create_user(user: Annotated[CreateUser, Depends()]):
    return dal.create_user(user_data=user)
