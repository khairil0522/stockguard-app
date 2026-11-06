from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.inventory import InventoryListRead, InventoryDetailRead
from app.services.inventory_service import get_all_inventory, get_inventory_by_id
from app.errors.inventory import InventoryNotFoundError

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get(
    "",
    response_model=list[InventoryListRead],
    status_code=status.HTTP_200_OK,
)
async def get_inventory(db: AsyncSession = Depends(get_db)):
    try:
        return await get_all_inventory(db)
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get(
    "/{product_id}",
    response_model=InventoryDetailRead,
    status_code=status.HTTP_200_OK,
)
async def get_inventory_detail(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_inventory_by_id(db, product_id)
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )