from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Inventory, Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.errors.product import DuplicateSKUError, ProductNotFoundError, ProductHasStockError, ProductInactiveError
from app.errors.inventory import InventoryNotFoundError

from app.services.storage_service import storage_service
from app.services.audit_log_service import AuditLogService

class ProductService:
    async def create(
        self,
        db: AsyncSession,
        payload: ProductCreate,
        user_id: UUID,
    ) -> Product:

        existing_product = await db.scalar(
            select(Product).where(Product.sku == payload.sku)
        )

        if existing_product is not None:
            await AuditLogService.log(
                db,
                actor_type="USER",
                user_id=user_id,
                event_type="SECURITY",
                action="CREATE_PRODUCT_FAILED",
                entity_type="PRODUCT",
                description=(
                    f"Failed to create product with SKU {payload.sku}: "
                    "SKU already exists"
                ),
                severity="LOW",
                event_metadata={
                    "sku": payload.sku,
                },
            )

            await db.commit()

            raise DuplicateSKUError(
                f"SKU {payload.sku} sudah digunakan oleh produk lain."
            )

        try:
            async with db.begin():
                product = Product(
                    sku=payload.sku,
                    name=payload.name,
                    unit_price=payload.unit_price,
                    description=payload.description,
                    is_active=True,
                )

                db.add(product)
                await db.flush()

                inventory = Inventory(
                    product_id=product.id,
                    on_hand=0,
                    reserved_qty=0,
                )

                db.add(inventory)
                await db.flush()

                await AuditLogService.log(
                    db,
                    actor_type="USER",
                    user_id=user_id,
                    event_type="ACTIVITY",
                    action="CREATE_PRODUCT",
                    entity_type="PRODUCT",
                    entity_id=product.id,
                    description=f"Product {product.sku} created",
                    severity="INFO",
                    event_metadata={
                        "sku": product.sku,
                        "name": product.name,
                    },
                )

            return product

        except IntegrityError as exc:
            constraint = getattr(
                getattr(exc.orig, "diag", None),
                "constraint_name",
                None,
            )

            if constraint and "sku" in constraint.lower():
                raise DuplicateSKUError(
                    f"SKU {payload.sku} sudah digunakan oleh produk lain."
                ) from exc

            raise


    async def get_all(self, db: AsyncSession):
        statement = select(Product).order_by(Product.name)
        result = await db.scalars(statement)
        products = result.all()

        return products


    async def get_detail(self, db: AsyncSession, product_id : UUID):
        statement = (
            select(Product)
            .options(selectinload(Product.inventory))
            .where(Product.id == product_id)
        )
        product = await db.scalar(statement)
        if product is None:
            raise ProductNotFoundError()
        
        return product


    async def update(
        self,
        db: AsyncSession,
        product_id : UUID,
        payload : ProductUpdate,
        user_id : UUID,
    ):
        product = await db.get(Product, product_id)

        if product is None:
            await AuditLogService.log(
                db,
                actor_type="USER",
                user_id=user_id,
                event_type="SECURITY",
                action="UPDATE_PRODUCT_FAILED",
                entity_type="PRODUCT",
                description="Failed to update product: product not found",
                severity="LOW",
                event_metadata={
                    "product_id": str(product_id),
                },
            )

            await db.commit()
            raise ProductNotFoundError()
        
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        await AuditLogService.log(
            db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="UPDATE_PRODUCT",
            entity_type="PRODUCT",
            entity_id=product.id,
            description=f"Product {product.sku} updated",
            severity="INFO",
            event_metadata={
                "updated_fields": list(update_data.keys()),
            },
        )

        await db.commit()
        await db.refresh(product)

        return product


    async def update_status(
        self,
        db: AsyncSession,
        product_id: UUID,
        is_active: bool,
        user_id: UUID,
    ):
        product = await db.get(Product, product_id)

        if product is None:
            await AuditLogService.log(
                db,
                actor_type="USER",
                user_id=user_id,
                event_type="SECURITY",
                action="UPDATE_PRODUCT_STATUS_FAILED",
                entity_type="PRODUCT",
                description="Failed to update product status: product not found",
                severity="LOW",
                event_metadata={
                    "product_id": str(product_id),
                    "requested_status": is_active,
                },
            )

            await db.commit()
            
            raise ProductNotFoundError()

        inventory = await db.scalar(
            select(Inventory).where(Inventory.product_id == product_id).with_for_update()
        )

        if not is_active:
            if inventory is None:
                raise InventoryNotFoundError()

            if inventory.on_hand > 0 or inventory.reserved_qty > 0:
                await AuditLogService.log(
                    db,
                    actor_type="USER",
                    user_id=user_id,
                    event_type="SECURITY",
                    action="DEACTIVATE_PRODUCT_FAILED",
                    entity_type="PRODUCT",
                    entity_id=product.id,
                    description="Failed to deactivate product: product has stock",
                    severity="LOW",
                    event_metadata={
                        "product_id": str(product.id),
                        "on_hand": inventory.on_hand,
                        "reserved_qty": inventory.reserved_qty,
                    },
                )

                await db.commit()
                raise ProductHasStockError("Produk masih memiliki stok yang tersedia dan tidak dapat dinonaktifkan.")
        
        previous_status = product.is_active
        product.is_active = is_active

        action = (
            "ACTIVATE_PRODUCT"
            if is_active
            else "DEACTIVATE_PRODUCT"
        )

        await AuditLogService.log(
            db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action=action,
            entity_type="PRODUCT",
            entity_id=product.id,
            description=f"Product {product.sku} status changed",
            severity="INFO",
            event_metadata={
                "previous_status": previous_status,
                "new_status": is_active,
            },
        )

        await db.commit()
        await db.refresh(product)

        if product.is_active == is_active:
            return product


    async def upload_image(self, db: AsyncSession, product_id: UUID, file_content: bytes, content_type: str, user_id: UUID):
        product = await db.get(Product, product_id)

        if product is None:
            raise ProductNotFoundError()

        object_key = f"products/{product_id}/main.  jpg"

        storage_service.upload(
            file_content=file_content,
            object_key=object_key,
            content_type=content_type,
        )

        product.image_key = object_key

        await AuditLogService.log(
            db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="UPLOAD_PRODUCT_IMAGE",
            entity_type="PRODUCT",
            entity_id=product.id,
            description=f"Product image uploaded for {product.sku}",
            severity="INFO",
            event_metadata={
                "content_type": content_type,
            },
        )

        await db.commit()
        await db.refresh(product)

        return product


    async def get_image_url(self, db: AsyncSession, product_id: UUID):
        product = await db.get(Product, product_id)

        if product is None: 
            raise ProductNotFoundError()

        if product.image_key is None:
            return None

        return storage_service.generate_presigned_url(
            object_key=product.image_key,
        )


    async def delete_image(
        self,
        db: AsyncSession,
        product_id: UUID,
        user_id: UUID,
    ):
        product = await db.get(Product, product_id)

        if product is None:
            raise ProductNotFoundError()

        if not product.is_active:
            raise ProductInactiveError(
                "Image produk yang tidak aktif tidak dapat dihapus."
            )

        if product.image_key is None:
            raise ProductImageNotFoundError()

        image_key = product.image_key

        storage_service.delete(image_key)

        product.image_key = None #image key harus dikosongkan mengingat foto sudah dihapus dari S3

        await AuditLogService.log(
            db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="DELETE_PRODUCT_IMAGE",
            entity_type="PRODUCT",
            entity_id=product.id,
            description=f"Product image deleted for {product.sku}",
            severity="INFO",
            event_metadata={
                "image_key": image_key,
            },
        )

        await db.commit()
        await db.refresh(product)

        return product



product_service = ProductService()