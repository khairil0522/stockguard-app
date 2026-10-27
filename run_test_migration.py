
import os
from dotenv import dotenv_values
from alembic.config import Config
from alembic import command

test_env = dotenv_values(".env.test")
database_url = test_env.get("database_url")

if not database_url:
    raise RuntimeError("database_url tidak ditemukan di .env.test")

if not database_url.endswith("/stockguard_test_db"):
    raise RuntimeError("Dibatalkan: URL bukan stockguard_test_db")

os.environ["DATABASE_URL"] = database_url

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

print("Migrasi database testing selesai.")
