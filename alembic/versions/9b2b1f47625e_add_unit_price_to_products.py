"""add unit price to products

Revision ID: 9b2b1f47625e
Revises: 6d78bff42a99
Create Date: 2026-10-17 23:08:06.626221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b2b1f47625e'
down_revision: Union[str, Sequence[str], None] = '6d78bff42a99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("unit_price", sa.Integer(), nullable=False),
    )

    op.create_check_constraint(
        "ck_products_unit_price_nonnegative",
        "products",
        "unit_price >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_products_unit_price_nonnegative",
        "products",
        type_="check",
    )
    op.drop_column("products", "unit_price")
