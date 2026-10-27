import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, String, func, CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class BookingItem(Base):
    __tablename__ = "booking_items"

    __table_args__ = (
        CheckConstraint(
            "qty > 0",
            name="ck_items_qty_positive"
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_items_unit_price_nonnegative"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="RESTRICT"),
        nullable=False
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False
    )

    qty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    booking: Mapped["Booking"] = relationship(
        "Booking",
        back_populates="items",
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="booking_items",
    )