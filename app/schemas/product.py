from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID

class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)
    unit_price: int
    description: str | None = None

class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    sku: str
    name: str
    description: str | None
    unit_price : int
    is_active: bool
