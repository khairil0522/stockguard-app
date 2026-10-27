import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, func

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        CheckConstraint(
            "on_hand >= 0",
            name="ck_inventory_on_hand_nonnegative"
        ),
        CheckConstraint(
            "reserved_qty >= 0",
            name="ck_inventory_reserved_nonnegative"
        ),
        CheckConstraint(
            "reserved_qty <= on_hand",
            name="ck_inventory_reserved_lte_on_hand"
        ),
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        primary_key=True,
    )

    on_hand: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    reserved_qty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inventory",
    )

    @property
    def available_qty(self) -> int:
        return self.on_hand - self.reserved_qty