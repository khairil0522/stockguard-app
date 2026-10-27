from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import create_product_with_inventory
from app.errors.product import DuplicateSKUError

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
            message=exc.message,
            error_code = exc.error_code,
            detail = exc.detail
        )
