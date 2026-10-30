from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductDetailRead, ProductUpdate
from app.services.product_service import create_product_with_inventory, get_detail_product, get_all_products, update_product_without_inventory, remove_product
from app.errors.product import DuplicateSKUError, ProductNotFoundError
from app.models.products import Product

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_product_with_inventory(db, payload)
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
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductDetailRead,
    status_code=status.HTTP_200_OK,
)
def get_product_detail(
    product_id : UUID,
    db: Session = Depends(get_db),
):
    try:
        return get_detail_product(db, product_id)
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
def update_product(
    payload: ProductUpdate,
    product_id : UUID,
    db: Session = Depends(get_db),
):
    try:
        return update_product_without_inventory(db, product_id, payload)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )

@router.delete(
    "/{product_id}",
    response_model=ProductRead,
    status_code=status.HTTP_200_OK,
)
def delete_product(
    product_id : UUID,
    db: Session = Depends(get_db)
):
    try:
        return remove_product(db, product_id)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )