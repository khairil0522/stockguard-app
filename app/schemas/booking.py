import uuid
from pydantic import BaseModel, Field

class BookingItemCreate(BaseModel):
    product_id : uuid.UUID
    qty : int = Field(gt=0)

class BookingCreate(BaseModel):
    items : list[BookingItemCreate] = Field(min_length=1)