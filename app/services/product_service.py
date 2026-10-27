from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Inventory, Product
from app.schemas.product import ProductCreate
from app.errors.product import DuplicateSKUError

def create_product_with_inventory(
    db: Session,
    payload: ProductCreate,
    ) -> Product:
    try:
        with db.begin():
            existing_product = db.scalar(
                select(Product).where(Product.sku == payload.sku)
            )

            if existing_product is not None:
                raise DuplicateSKUError(payload.sku)

            product = Product(
                sku=payload.sku,
                name=payload.name,
                unit_price=payload.unit_price,
                description=payload.description,
                is_active=True,
            )

            db.add(product)
            db.flush()

            inventory = Inventory(
                product_id=product.id,
                on_hand=0,
                reserved_qty=0,
            )

            db.add(inventory)
            db.flush()

        return product

    except IntegrityError as exc:
        # Menangani kemungkinan dua request membuat SKU
        # yang sama secara bersamaan.
        constraint = getattr(
            getattr(exc.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint and "sku" in constraint.lower():
            raise DuplicateSKUError(payload.sku) from exc

        raise