from typing import Annotated

from fastapi import Path, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from core.models import Product, db_manager


async def product_by_id(
    product_id: Annotated[int, Path(...)],
    session: Annotated[AsyncSession, Depends(db_manager.session_scoped_dep)],
) -> Product:
    product = await crud.get_product_by_id(
        product_id=product_id,
        session=session,
    )

    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found",
    )
