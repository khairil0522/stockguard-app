from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StockAdjustmentCreate(BaseModel):
    movement_type: Literal["INCREASE", "DECREASE"]
    quantity: int = Field(gt=0)
    reason: str = Field(min_length=1, max_length=255)


class StockAdjustmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    movement_type: Literal["INCREASE", "DECREASE"]
    quantity: int
    previous_on_hand: int
    new_on_hand: int
    available_qty: int
    reason: str

class StockAdjustmentHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID
    movement_type: Literal["INCREASE", "DECREASE"]
    quantity: int
    previous_on_hand: int
    new_on_hand: int
    reason: str
    product_name: str
