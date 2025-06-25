from users.schemas import CreateUser


def create_user(user_data: CreateUser) -> dict:
    user = user_data.model_dump()
    return {
        "success": True,
        "user": user
    }