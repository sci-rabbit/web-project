from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from core.models.order_product_association import OrderProductAssociation


class Product(Base):

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product"
    )
