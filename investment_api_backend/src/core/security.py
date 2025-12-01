from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=[settings.PASSWORD_HASH_SCHEME], deprecated="auto")


def _bcrypt_safe_truncate(password: str) -> str:
    """
    Truncate the password to 72 bytes to align with bcrypt's effective input limit.
    This ensures consistent hashing/verification even if Unicode characters expand
    to more than one byte in UTF-8.
    """
    if password is None:
        return ""
    password_bytes = password.encode("utf-8")
    truncated = password_bytes[:72]
    return truncated.decode("utf-8", errors="ignore")


# PUBLIC_INTERFACE
def get_password_hash(password: str) -> str:
    """Return a secure password hash using passlib.

    Note: We truncate to 72 bytes prior to hashing to match bcrypt's input limit.
    """
    safe = _bcrypt_safe_truncate(password)
    return pwd_context.hash(safe)


# PUBLIC_INTERFACE
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash.

    Note: We truncate to 72 bytes prior to verification to match hashing behavior.
    """
    safe = _bcrypt_safe_truncate(plain_password)
    return pwd_context.verify(safe, hashed_password)


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
