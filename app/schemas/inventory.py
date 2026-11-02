from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    on_hand: int
    reserved_qty: int
    available_qty: int

class InventoryListRead(BaseModel):
    product_id: UUID
    sku: str
    product_name: str
    on_hand: int
    available_qty: int

    model_config = ConfigDict(from_attributes=True)

class InventoryDetailRead(BaseModel):
    product_id: UUID
    sku: str
    product_name: str
    on_hand: int
    reserved_qty: int
    description: str | None = None
    available_qty: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)