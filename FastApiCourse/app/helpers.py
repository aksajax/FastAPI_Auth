from pwdlib import PasswordHash
from datetime import datetime, timedelta,timezone
from jose import jwt
from app.config.app_config import get_app_config

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    PasswordHash = PasswordHash.recommended()
    return PasswordHash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    PasswordHash = PasswordHash.recommended()
    return PasswordHash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = 15):
    """Create a JWT access token."""
    config = get_app_config()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode a JWT access token."""
    config = get_app_config()
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
        return payload
    except jwt.JWTError:
        return None