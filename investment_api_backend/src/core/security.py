from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

from src.core.config import get_settings

settings = get_settings()

# Initialize a single Argon2 PasswordHasher instance.
# Defaults are strong and suitable for most applications; tune if needed via env in future.
_argon2_hasher = PasswordHasher()


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Return a secure password hash using Argon2id."""
    # Argon2 has no 72-byte limit; do not truncate.
    return _argon2_hasher.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2 hash."""
    try:
        return _argon2_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False


# PUBLIC_INTERFACE
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token for a given subject (user id or email)."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# PUBLIC_INTERFACE
def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT and return the subject if valid, else None."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
