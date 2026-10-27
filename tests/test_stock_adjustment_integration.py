import pytest

from uuid import uuid4

from sqlalchemy import select

from app.models import Product, Inventory, StockMovement
from app.schemas.stock_movement import StockAdjustmentCreate
from app.services.stock_adjustment_service import adjust_stock, InsufficientStockError

def test_increase_stock_persist_to_db(db_session):
    # Arrange: buat produk dan stok awal
    product = Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Integration Test Product",
        unit_price=100000
    )

    db_session.add(product)
    db_session.flush()

    inventory = Inventory(
        product_id=product.id,
        on_hand=10,
        reserved_qty=0,
    )
    db_session.add(inventory)
    db_session.flush()

    # Penting: akhiri transaksi setup agar service
    # bisa memulai transaksi menggunakan db.begin()
    db_session.commit()

    # Act: tambah stok sebanyak 5 unit
    payload = StockAdjustmentCreate(
        movement_type="INCREASE",
        quantity=5, 
        reason="Integration test",
    )

    movement = adjust_stock(db_session, product.id, payload)

    #Assert: cek stok terbaru dari db
    db_session.refresh(inventory)
    assert inventory.on_hand == 15

    #Assert: cek riwayat pergerakan stok
    saved_movement = db_session.scalar(
        select(StockMovement).where(StockMovement.id == movement.id)
    )

    assert saved_movement is not None
    assert saved_movement.quantity == 5
    assert saved_movement.previous_on_hand == 10
    assert saved_movement.new_on_hand == 15

def test_decrease_stock_persist_to_db(db_session):
    #Arrage: buat produk dan stok awal
    product = Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Integration Test Product",
        unit_price=100000
    )

    db_session.add(product)
    db_session.flush()

    inventory = Inventory(
        product_id=product.id,
        on_hand=20,
        reserved_qty=0,
    )
    db_session.add(inventory)
    db_session.flush()

    # Penting: akhiri transaksi setup agar service
    # bisa memulai transaksi menggunakan db.begin()
    db_session.commit()

    # Act: kurangi stok sebanyak 5 unit
    payload = StockAdjustmentCreate(
        movement_type = "DECREASE",
        quantity=5,
        reason="Pengambilan Stok"
    )

    movement = adjust_stock(db_session, product.id, payload)

    # Assert: Cek stok dari db
    db_session.refresh(inventory)
    assert inventory.on_hand == 15

    # Assert: cek riwayat pergerakan stok
    saved_movement = db_session.scalar(
        select(StockMovement).where(StockMovement.id == movement.id)
    )

    assert movement is not None
    assert saved_movement.quantity == 5
    assert saved_movement.previous_on_hand == 20
    assert saved_movement.new_on_hand == 15

def test_decrease_insufficient_stock(db_session):
    product = Product(
        sku=f"TEST-{uuid4().hex[:8]}",
        name="Integration Test Product",
        unit_price=100000
    )

    db_session.add(product)
    db_session.flush()

    inventory = Inventory(
        product_id = product.id,
        on_hand=3,
        reserved_qty=2
    )

    db_session.add(inventory)
    db_session.flush()

    db_session.commit()

    payload = StockAdjustmentCreate(
        movement_type = "DECREASE",
        quantity = 5,
        reason="ambil stok"
    )

    with pytest.raises(InsufficientStockError):
        adjust_stock(db_session, product.id, payload)

    db_session.refresh(inventory)
    assert inventory.on_hand == 3
    assert inventory.reserved_qty == 2

    movement = db_session.scalars(
        select(StockMovement).where(StockMovement.product_id == product.id)
        ).all()

    assert len(movement) == 0
