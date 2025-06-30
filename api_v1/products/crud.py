from sqlalchemy import select, update, delete
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import Product


async def get_products(session: AsyncSession) -> list[Product]:
    query = select(Product).order_by(Product.id)
    result: Result = await session.execute(query)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(product_id: int, session: AsyncSession) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def product_update(
    product: Product,
    product_upd: ProductUpdate | ProductUpdatePartial,
    session: AsyncSession,
    partial: bool = False,
) -> Product:
    for name, value in product_upd.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)

    await session.commit()
    return product


async def product_delete(product: Product, session: AsyncSession) -> None:
    await session.delete(product)
    await session.commit()
