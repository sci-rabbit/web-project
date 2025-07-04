from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models.order_product_association import OrderProductAssociation


class Order(Base):

    promo_code: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )

    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order"
    )
