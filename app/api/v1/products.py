from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductDetailRead, ProductUpdate, ProductStatusUpdate, ProductResponse
from app.services.product_service import create_product_with_inventory, get_detail_product, get_all_products, update_product_without_inventory, restatus_product
from app.errors.product import DuplicateSKUError, ProductNotFoundError, ProductHasStockError, ProductInactiveError

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_product_with_inventory(db, payload)
    except DuplicateSKUError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )


@router.get(
    "",
    response_model=list[ProductRead],
    status_code=status.HTTP_200_OK,
)
async def get_products(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductDetailRead,
    status_code=status.HTTP_200_OK,
)
async def get_product_detail(
    product_id : UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await get_detail_product(db, product_id)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )

@router.put(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    payload: ProductUpdate,
    product_id : UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await update_product_without_inventory(db, product_id, payload)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )

@router.patch(
    "/{product_id}/status",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
)
async def update_product_status(
    product_id : UUID,
    payload: ProductStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        return await restatus_product(db, product_id, payload.is_active)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )
    except ProductHasStockError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )
    except ProductInactiveError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )