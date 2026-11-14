from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductDetailRead, ProductUpdate, ProductStatusUpdate, ProductResponse
from app.services.product_service import product_service
from app.errors.product import DuplicateSKUError, ProductNotFoundError, ProductHasStockError, ProductInactiveError
from app.dependencies.auth import require_permission, get_current_user

from app.models.users import User

router = APIRouter(prefix="/products", tags=["Products"])
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post(
    "",
    response_model=ProductRead,
    dependencies=[Depends(require_permission("product.create"))],
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    payload: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await product_service.create(db, payload, current_user.id)
    except DuplicateSKUError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )


@router.get(
    "",
    response_model=list[ProductRead],
    dependencies=[Depends(require_permission("product.read"))],
    status_code=status.HTTP_200_OK,
)
async def get_products(db: AsyncSession = Depends(get_db)):
    return await product_service.get_all(db)


@router.get(
    "/{product_id}",
    response_model=ProductDetailRead,
    dependencies=[Depends(require_permission("product.read"))],
    status_code=status.HTTP_200_OK,
)
async def get_product_detail(
    product_id : UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await product_service.get_detail(db, product_id)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )

@router.put(
    "/{product_id}",
    response_model=ProductRead,
    dependencies=[Depends(require_permission("product.update"))],
    status_code=status.HTTP_200_OK,
)
async def update_product(
    payload: ProductUpdate,
    product_id : UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user), 
):
    try:
        return await product_service.update(db, product_id, payload, current_user.id)
    except ProductNotFoundError as exc :
        raise HTTPException(
            status_code=exc.status_code,
            detail = exc.detail
        )

@router.patch(
    "/{product_id}/status",
    response_model=ProductResponse,
    dependencies=[Depends(require_permission("product.status"))],
    status_code=status.HTTP_200_OK,
)
async def update_product_status(
    product_id : UUID,
    payload: ProductStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return await product_service.update_status(db, product_id, payload.is_active, current_user.id)
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


@router.post(
    "/{product_id}/image",
    dependencies=[Depends(require_permission("product.create"))],)
async def upload_product_image(
    product_id: UUID,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="File harus berupa JPEG, PNG, atau WebP.",
        )

    file_content = await file.read()

    if len(file_content) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Ukuran file maksimal 5 MB.",
        )

    return await product_service.upload_image(
        db=db,
        product_id=product_id,
        file_content=file_content,
        content_type=file.content_type,
        user_id=current_user.id
    )


@router.get(
    "/{product_id}/image",
    dependencies=[Depends(require_permission("product.read"))],
    status_code=status.HTTP_200_OK,
)
async def get_product_image(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        image_url = await product_service.get_image_url(
            db=db,
            product_id=product_id,
        )

        if image_url is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product image not found.",
            )

        return {
            "image_url": image_url
        }

    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )


@router.delete(
    "/{product_id}/image",
    dependencies=[Depends(require_permission("product.update"))],
    status_code=status.HTTP_200_OK,
)
async def delete_product_image(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await product_service.delete_image(
            db=db,
            product_id=product_id,
            user_id=current_user.id,
        )

    except ProductNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except ProductInactiveError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )

    except ProductImageNotFoundError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail,
        )