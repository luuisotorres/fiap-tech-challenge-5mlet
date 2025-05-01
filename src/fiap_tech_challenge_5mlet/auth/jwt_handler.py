import jwt
import datetime
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config import settings

# HTTPBearer scheme
security = HTTPBearer()


def create_token(username: str) -> str:
    """
    Generate a JWT token for a given username.

    Args:
        username (str): Username to embed in token payload.

    Returns:
        str: Encoded JWT token.
    """
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(
            seconds=settings.jwt_exp_delta_seconds
        )
    }
    return jwt.encode(payload, settings.jwt_secret_key,
                      algorithm=settings.jwt_algorithm)


def require_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    FastAPI dependency to validate JWT token from Authorization header.

    Args:
        credentials (HTTPAuthorizationCredentials): The bearer token.

    Returns:
        dict: Decoded JWT payload.

    Raises:
        HTTPException: If token is missing, expired, or invalid.
    """
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        payload = jwt.decode(token, settings.jwt_secret_key,
                             algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def authenticate_user(username: str, password: str) -> bool:
    """
    Validate login credentials against .env-based test user.

    Args:
        username (str): Supplied username.
        password (str): Supplied password.

    Returns:
        bool: True if credentials match, False otherwise.
    """
    return (username == settings.test_username
            and password == settings.test_password)
