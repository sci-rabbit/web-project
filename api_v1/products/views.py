from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.dependecies import product_by_id
from api_v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from core.models import db_manager

router = APIRouter(tags=["Products CRUD"])

db_session = Annotated[AsyncSession, Depends(db_manager.session_scoped_dep)]


@router.get("/")
async def get_products(
    session: db_session,
) -> list[Product]:
    return await crud.get_products(session=session)


@router.post("/")
async def create_product(
    product_data: Annotated[ProductCreate, Depends()],
    session: db_session,
) -> Product:
    return await crud.create_product(
        session=session,
        product_data=product_data,
    )


@router.get("/{product_id}/")
async def get_product_by_id(
    product: Annotated[Product, Depends(product_by_id)],
) -> Product:
    return product


@router.put("/{product_id}/")
async def product_update(
    product: Annotated[Product, Depends(product_by_id)],
    product_upd: ProductUpdate,
    session: db_session,
) -> Product:
    product = await crud.product_update(
        product=product,
        product_upd=product_upd,
        session=session,
    )

    return product


@router.patch("/{product_id}/")
async def product_update_partial(
    product: Annotated[Product, Depends(product_by_id)],
    product_upd: ProductUpdatePartial,
    session: db_session,
) -> Product:
    product = await crud.product_update(
        product=product, product_upd=product_upd, session=session, partial=True
    )

    return product


@router.delete("/{product_id}/")
async def product_delete(
    product: Annotated[Product, Depends(product_by_id)],
    session: db_session,
) -> None:
    await crud.product_delete(product=product, session=session)
