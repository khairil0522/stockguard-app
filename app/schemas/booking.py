import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.bookings import BookingStatus

class BookingItemCreate(BaseModel):
    product_id : uuid.UUID
    qty : int = Field(gt=0)

class BookingCreate(BaseModel):
    items : list[BookingItemCreate] = Field(min_length=1)

class BookingItemRead(BaseModel):
    product_id: uuid.UUID
    qty: int
    unit_price: int

    model_config = ConfigDict(from_attributes=True)


class BookingRead(BaseModel):
    id: uuid.UUID
    booking_code: str
    booking_status: BookingStatus
    user_id: uuid.UUID
    expired_at: datetime
    created_at: datetime
    updated_at: datetime
    items: list[BookingItemRead]

    model_config = ConfigDict(from_attributes=True)