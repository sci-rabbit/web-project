from fastapi import APIRouter

from .products.views import router as product_router

router = APIRouter(prefix="/products")
router.include_router(router=product_router)
