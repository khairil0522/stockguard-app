from app.services.audit_log_service import AuditLogService


class UserAudit:

    def __init__(self, db):
        self.db = db

    async def create(self, actor_id, user_id, username, role_name ):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="ACTIVITY",
            action="CREATE_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was created",
            severity="INFO",
            event_metadata={
                "role": role_name,
            },
        )

    async def update(self, actor_id, user_id, username, updated_fields):
        event_metadata = {
            "updated_fields": updated_fields,
        }

        if "password" in updated_fields:
            event_metadata["password_changed"] = True

        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="ACTIVITY",
            action="UPDATE_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was updated",
            severity="INFO",
            event_metadata=event_metadata,
        )


    async def block(self, actor_id, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="SECURITY",
            action="BLOCK_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was blocked",
            severity="MEDIUM",
        )

    async def unblock(self, actor_id, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="SECURITY",
            action="UNBLOCK_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was unblocked",
            severity="MEDIUM",
        )

    async def deactivate(self, actor_id, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="SECURITY",
            action="DEACTIVATE_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was deactivated",
            severity="MEDIUM",
        )

    async def reactivate(self, actor_id, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=actor_id,
            event_type="SECURITY",
            action="REACTIVATE_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} was reactivated",
            severity="MEDIUM",
        )