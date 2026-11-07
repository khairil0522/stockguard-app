from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

# Password hashing menggunakan Argon2
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Mengubah plain-text password menjadi password hash.
    Hash inilah yang disimpan ke database.
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Memverifikasi plain-text password terhadap hash
    yang tersimpan di database.
    """
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: str) -> str:
    """
    Membuat JWT access token yang membawa identitas user.
    """
    expire_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": user_id,
        "exp": expire_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> str:
    """
    Memverifikasi JWT dan mengambil user_id dari claim 'sub'.

    Akan melempar exception jika token tidak valid
    atau sudah expired.
    """
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    user_id = payload.get("sub")

    if not user_id:
        raise ValueError("Token tidak memiliki subject.")

    return user_id