from pydantic import BaseModel, ConfigDict, Field

class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    on_hand: int
    reserved_qty: int
    available_qty: int