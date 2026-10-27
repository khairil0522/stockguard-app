from pydantic import BaseModel

class DashboardStatsResponse(BaseModel):
    total_products: int
    available_stock: int