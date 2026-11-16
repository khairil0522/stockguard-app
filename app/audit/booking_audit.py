from app.services.audit_log_service import AuditLogService

class BookingAudit:

    def __init__(self, db):
        self.db = db

    async def create(self, user_id, booking_id, booking_code, item_count, expired_at):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CREATE_BOOKING",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_code} created",
            severity="INFO",
            event_metadata={
                "booking_code": booking_code,
                "item_count": item_count,
                "expired_at": expired_at.isoformat(),
            },
        )

    async def confirm(self, user_id, booking_id, booking_code):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CONFIRM_BOOKING",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_code} confirmed",
            severity="INFO",
        )

    async def confirm_failed(self, user_id, booking_id, booking_code):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CONFIRM_BOOKING_FAILED",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_code} cannot be confirmed",
            severity="MEDIUM",
        )

    async def cancel(self, user_id, booking_id, booking_code):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CANCEL_BOOKING",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_code} cancelled",
            severity="INFO",
        )

    async def cancel_failed(self, user_id, booking_id, booking_code):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="CANCEL_BOOKING_FAILED",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_code} cannot be cancelled",
            severity="MEDIUM",
        )

    async def expire(self, booking_id):
        await AuditLogService.log(
            self.db,
            actor_type="SYSTEM",
            event_type="ACTIVITY",
            action="EXPIRE_BOOKING",
            entity_type="BOOKING",
            entity_id=booking_id,
            description=f"Booking {booking_id} expired automatically",
            severity="INFO",
        )