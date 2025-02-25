from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import secrets

JWT_SECRET = secrets.token_hex(16)
JWT_ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(name: str, email: str, expires_delta: timedelta):
    payload = {"email": email, "name": name}
    expires = datetime.now(timezone.utc)+expires_delta
    payload.update({"exp": expires.timestamp()})
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode(token: str = Depends(oauth2_scheme)):
    try:
        decode_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def get_password_hash(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def verify_password(plain_pwd: str, hashed_pwd: bytes):
    if bcrypt.checkpw(plain_pwd.encode("utf-8"), hashed_pwd):
        return True
    return False
