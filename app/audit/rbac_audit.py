from app.services.audit_log_service import AuditLogService

class RBACAudit:

    def __init__(self, db, actor_id, target_id, target_type):
        self.db = db
        self.actor_id = actor_id
        self.target_id = target_id
        self.target_type = target_type

    async def assign_role(self, role_name, before: dict | None = None, after: dict | None = None):
        
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=self.actor_id,
            event_type="ACTIVITY",
            action="ASSIGN_ROLE",
            entity_type=self.target_type,
            entity_id=self.target_id,
            description=f"Role {role_name} assigned to {self.target_type.lower()}",
            event_metadata={
                "role_name": role_name,
                "before": before,
                "after": after,
            },
            severity="INFO",
        )

    async def revoke_role(self, role_name, before: dict | None = None, after: dict | None = None):

        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=self.actor_id,
            event_type="ACTIVITY",
            action="REVOKE_ROLE",
            entity_type=self.target_type,
            entity_id=self.target_id,
            description=f"Role {role_name} revoked from {self.target_type.lower()}",
            event_metadata={
                "role_name": role_name,
                "before": before,
                "after": after,
            },
            severity="INFO",
        )

    async def grant_permission(self, permission_name: str, before: dict | None = None, after: dict | None = None):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=self.actor_id,
            event_type="ACTIVITY",
            action="GRANT_PERMISSION",
            entity_type=self.target_type,
            entity_id=self.target_id,
            description=f"Permission {permission_name} granted to {self.target_type.lower()}",
            event_metadata={
                "permission_name": permission_name,
                "before": before,
                "after": after,
            },
            severity="INFO",
        )

    async def revoke_permission(self,permission_name: str,before: dict | None = None,after: dict | None = None):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=self.actor_id,
            event_type="ACTIVITY",
            action="REVOKE_PERMISSION",
            entity_type=self.target_type,
            entity_id=self.target_id,
            description=f"Permission {permission_name} revoked from {self.target_type.lower()}",
            event_metadata={
                "permission_name": permission_name,
                "before": before,
                "after": after,
            },
            severity="INFO",
        )