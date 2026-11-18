from sqlalchemy.orm import configure_mappers

from app.models.users import User
from app.models.roles import Role
from app.models.permissions import Permission
from app.models.user_roles import UserRole
from app.models.role_permissions import RolePermission
from app.models.user_customers import UserCustomer

configure_mappers()

print("All model relationships configured successfully!")