from app.services.audit_log_service import AuditLogService


class AdjustmentAudit:

    def __init__(self, db):
        self.db = db

    async def adjust(self, user_id, product_id, sku, movement_type, quantity, previous_on_hand, new_on_hand, reserved_qty, reason):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="ADJUST_STOCK",
            entity_type="PRODUCT",
            entity_id=product_id,
            description=f"Stock adjusted for product {sku}",
            severity="INFO",
            event_metadata={
                "movement_type": movement_type,
                "quantity": quantity,
                "previous_on_hand": previous_on_hand,
                "new_on_hand": new_on_hand,
                "reserved_qty": reserved_qty,
                "reason": reason,
            },
        )

    async def adjust_failed(self, user_id, product_id, movement_type, quantity, reason):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="ADJUST_STOCK_FAILED",
            entity_type="PRODUCT",
            entity_id=product_id,
            description="Stock adjustment failed: insufficient available stock",
            severity="MEDIUM",
            event_metadata={
                "movement_type": movement_type,
                "quantity": quantity,
                "reason": reason,
            },
        )