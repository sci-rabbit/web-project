import uvicorn
from fastapi import FastAPI

from item_views import router as items_router
from users.views import router as users_router


app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
