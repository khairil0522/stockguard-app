from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies.auth import require_permission
from app.errors.inventory import InventoryNotFoundError
from app.schemas.inventory import InventoryDetailRead, InventoryListRead
from app.services.inventory_service import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])
DB_SESSION_DEPENDENCY = Depends(get_db)


@router.get(
    "",
    response_model=list[InventoryListRead],
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("inventory.read"))
    ],
)
async def get_inventory(db: AsyncSession = DB_SESSION_DEPENDENCY):
    try:
        return await inventory_service.get_all(db)
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )

@router.get(
    "/{product_id}",
    response_model=InventoryDetailRead,
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permission("inventory.read"))
    ],
)
async def get_inventory_detail(
    product_id: UUID,
    db: AsyncSession = DB_SESSION_DEPENDENCY,
):
    try:
        return await inventory_service.get_by_id(db, product_id)
    except InventoryNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )