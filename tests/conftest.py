import pytest

from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
import app.models

#Baca konfigurasi khusus testing
test_env = dotenv_values(".env.test")
test_database_url = test_env.get("database_url")

if not test_database_url:
    raise ValueError("Database url tidak diatur di .env.test")

if not test_database_url.split("@")[-1].endswith("stockguard_test_db"):
    raise RuntimeError(
        "Test harus menggunakan database stockguard_test_db"
    )

@pytest.fixture
def test_engine():
    test_engine = create_engine(test_database_url)

    try:
        yield test_engine
    finally:
        test_engine.dispose()

@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

        if transaction.is_active:
            transaction.rollback()
                
        connection.close()