from app.services.audit_log_service import AuditLogService


class ProductAudit:

    def __init__(self, db):
        self.db = db

    async def create_failed(self, user_id, sku):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="CREATE_PRODUCT_FAILED",
            entity_type="PRODUCT",
            description=f"Product with SKU {sku} cannot be created",
            severity="LOW",
            event_metadata={
                "sku": sku,
            },
        )

    async def create(self, user_id, product_id, sku, name):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CREATE_PRODUCT",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {sku} created",
            severity="INFO",
            event_metadata={
                "sku": sku,
                "name": name,
            },
        )

    async def update_failed(self, user_id, product_id):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="UPDATE_PRODUCT_FAILED",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {product_id} cannot be updated",
            severity="LOW",
            event_metadata={
                "product_id": product_id,
            },
        )

    async def update(self, user_id, product_id, sku, updated_fields):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="UPDATE_PRODUCT",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {sku} updated",
            severity="INFO",
            event_metadata={
                "updated_fields": updated_fields,
            },
        )

    async def update_status_failed(self, user_id, product_id, requested_status):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="UPDATE_PRODUCT_STATUS_FAILED",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {product_id} status update failed",
            severity="LOW",
            event_metadata={
                "product_id": product_id,
                "requested_status": requested_status,
            },
        )

    async def deactivate_failed(self, user_id, product_id, on_hand, reserved_qty):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="DEACTIVATE_PRODUCT_FAILED",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {product_id} cannot be deactivated",
            severity="LOW",
            event_metadata={
                "product_id": product_id,
                "on_hand": on_hand,
                "reserved_qty": reserved_qty,
            },
        )

    async def activate(self, user_id, product_id, sku, previous_status, new_status):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="ACTIVATE_PRODUCT",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {sku} activated",
            severity="INFO",
            event_metadata={
                "previous_status": previous_status,
                "new_status": new_status,
            },
        )

    async def deactivate(self, user_id, product_id, sku, previous_status, new_status):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="DEACTIVATE_PRODUCT",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Product {sku} deactivated",
            severity="INFO",
            event_metadata={
                "previous_status": previous_status,
                "new_status": new_status,
            },
        )

    async def upload_image(self, user_id, product_id, sku, content_type):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="UPLOAD_PRODUCT_IMAGE",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Image uploaded for product {sku}",
            severity="INFO",
            event_metadata={
                "content_type": content_type,
            },
        )

    async def delete_image(self, user_id, product_id, sku, image_key):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="DELETE_PRODUCT_IMAGE",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Image deleted from product {sku}",
            severity="INFO",
            event_metadata={
                "image_key": image_key,
            },
        )