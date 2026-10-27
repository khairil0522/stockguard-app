# ini sebuah test yang sederhana untuk menguji fungsi penyesuaian stok

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.models import Inventory
from app.schemas.stock_movement import StockAdjustmentCreate
from app.services.stock_adjustment_service import adjust_stock

def test_adjust_stock_propagates_flush_error():
    # Arrange: siapkan database session tiruan
    db = MagicMock()
    transaction = db.begin.return_value
    product_id = uuid4()

    inventory = Inventory(
        product_id=product_id,
        on_hand=10,
        reserved_qty=0,
    )
    db.scalar.return_value = inventory

    #Simulasikan kegagalan ketika SQLAlchemy mencoba melakukan flush ke db
    db.flush.side_effect = RuntimeError("Simulated database failure")

    Payload = StockAdjustmentCreate(
        movement_type="INCREASE",
        quantity=5,
        reason="Tes Rollback",
    )

    # Act & Assert: pastikan error harus keluar dari transaksi
    with pytest.raises(RuntimeError, match="Simulated database failure") as exc_info:
        adjust_stock(db, product_id, Payload)

    #Memastikan transaksi keluar karena exception
    assert transaction.__exit__.call_count == 1
    assert transaction.__exit__.call_args[0][0] is RuntimeError

def test_adjust_stock_rejects_decrease_below_reserved_quantity():
    from app.services.stock_adjustment_service import InsufficientStockError

    db = MagicMock()
    product_id = uuid4()

    inventory = Inventory(
        product_id=product_id,
        on_hand=10,
        reserved_qty=7,
    )

    db.scalar.return_value = inventory

    payload = StockAdjustmentCreate(
        movement_type="DECREASE",
        quantity=5,
        reason="Tes Stock tidak cukup",
    )

    with pytest.raises(InsufficientStockError):
        adjust_stock(db, product_id, payload)

    #Stock tidak boleh berubah sama sekali
    assert inventory.on_hand == 10

    #Tidak boleh ada stock movement baru
    db.add.assert_not_called()

def test_adjust_stock_increase_updates_inventory_and_creates_movement():
    db = MagicMock()
    product_id = uuid4()

    inventory = Inventory(
        product_id=product_id,
        on_hand=10,
        reserved_qty=2,
    )

    db.scalar.return_value = inventory

    payload = StockAdjustmentCreate(
        movement_type="INCREASE",
        quantity=5,
        reason="Restock barang",
    )

    movement = adjust_stock(db, product_id, payload)

    assert inventory.on_hand == 15
    db.add.assert_called_once()
    added_movement = db.add.call_args.args[0]

    assert added_movement.movement_type == "INCREASE"
    assert added_movement.quantity == 5
    assert added_movement.previous_on_hand == 10
    assert added_movement.new_on_hand == 15
    assert added_movement.reason == "Restock barang"
    assert movement is added_movement

def test_adjust_stock_raises_error_when_inventory_not_found():
    from app.services.stock_adjustment_service import ProductNotFoundError

    db = MagicMock()
    product_id = uuid4()
    db.scalar.return_value = None

    payload = StockAdjustmentCreate(
        movement_type="INCREASE",
        quantity=5,
        reason="Tes produk tidak ditemukan",
    )

    with pytest.raises(ProductNotFoundError):
        adjust_stock(db, product_id, payload)

    db.add.assert_not_called()
    db.flush.assert_not_called()