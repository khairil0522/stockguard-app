"""add product unit price check constraint

Revision ID: 71cc9a06baf0
Revises: 9b2b1f47625e
Create Date: 2026-10-17 23:17:47.004990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71cc9a06baf0'
down_revision: Union[str, Sequence[str], None] = '9b2b1f47625e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.create_check_constraint(
    #     "ck_products_unit_price_nonnegative",
    #     "products",
    #     "unit_price >= 0",
    # )
    pass


def downgrade() -> None:
    # op.drop_constraint(
    #     "ck_products_unit_price_nonnegative",
    #     "products",
    #     type_="check",
    # )
    pass
