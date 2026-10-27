import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Boolean, func, Text, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint(
            "unit_price >= 0",
            name="ck_products_unit_price_nonnegative"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    unit_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    # Relationships
    inventory: Mapped["Inventory | None"] = relationship(
        "Inventory",
        back_populates="product",
        uselist=False,
    )

    booking_items: Mapped[list["BookingItem"]] = relationship(
        "BookingItem",
        back_populates="product",
    )