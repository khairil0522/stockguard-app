from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Inventory, Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.errors.product import DuplicateSKUError, ProductNotFoundError, ProductHasStockError
from app.errors.inventory import InventoryNotFoundError

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
                raise DuplicateSKUError(f"SKU {payload.sku} sudah digunakan oleh produk lain.")

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
            raise DuplicateSKUError(
                f"SKU {payload.sku} sudah digunakan oleh produk lain."
            ) from exc

        raise

def get_all_products(db: Session):
    statement = select(Product).order_by(Product.name)
    products = db.scalars(statement).all()

    return products

def get_detail_product(db: Session, product_id : UUID):
    statement = (
        select(Product)
        .options(selectinload(Product.inventory))
        .where(Product.id == product_id)
    )   
    product = db.scalar(statement)
    if product is None:
        raise ProductNotFoundError()
    
    return product

def update_product_without_inventory(
    db: Session,
    product_id : UUID,
    payload : ProductUpdate
):
    product = db.get(Product, product_id)

    if product is None:
        raise ProductNotFoundError()
    
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

def restatus_product(
    db: Session,
    product_id: UUID,
    is_active: bool
):
    product = db.get(Product, product_id)

    if product is None:
        raise ProductNotFoundError()

    inventory = db.scalar(
        select(Inventory).where(Inventory.product_id == product_id).with_for_update()
    )

    if not is_active:
        if inventory is None:
            raise InventoryNotFoundError()

        if inventory.on_hand > 0 or inventory.reserved_qty > 0:
            raise ProductHasStockError("Produk masih memiliki stok yang tersedia dan tidak dapat dinonaktifkan.")
    
    product.is_active = is_active

    db.commit()
    db.refresh(product)

    return product