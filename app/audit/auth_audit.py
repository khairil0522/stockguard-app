from app.services.audit_log_service import AuditLogService


class AuthAudit:

    def __init__(self, db):
        self.db = db

    async def login_failed_system(self, username):
        await AuditLogService.log(
            self.db,
            actor_type="SYSTEM",
            event_type="SECURITY",
            action="LOGIN_FAILED",
            entity_type="USER",
            description="Login failed: invalid username or password",
            severity="LOW",
            event_metadata={
                "username": username,
            },
        )

    async def login_failed_user(self, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="LOGIN_FAILED",
            entity_type="USER",
            entity_id=user_id,
            description="Login failed: invalid username or password",
            severity="LOW",
            event_metadata={
                "username": username,
            },
        )

    async def login_success(self, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="SECURITY",
            action="LOGIN_SUCCESS",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} logged in successfully",
            severity="INFO",
        )

    async def register(self, user_id, username):
        await AuditLogService.log(
            self.db,
            actor_type="USER",
            user_id=user_id,
            event_type="ACTIVITY",
            action="REGISTER_USER",
            entity_type="USER",
            entity_id=user_id,
            description=f"User {username} registered",
        )

    async def register_failed(self, username, reason):
        await AuditLogService.log(
            self.db,
            actor_type="SYSTEM",
            event_type="SECURITY",
            action="REGISTER_FAILED",
            entity_type="USER",
            description="User registration failed",
            severity="LOW",
            event_metadata={
                "username": username,
                "reason": reason,
            },
        )