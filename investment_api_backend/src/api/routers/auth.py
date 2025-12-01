from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.core.config import get_settings
from src.core.security import create_access_token, decode_access_token
from src.db.crud import authenticate_user, create_user, get_user_by_email
from src.db.session import get_db
from src.schemas.auth import Token, UserCreate, UserLogin, UserPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])

security_bearer = HTTPBearer(auto_error=False)
settings = get_settings()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(security_bearer)],
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    sub = decode_access_token(token)
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = get_user_by_email(db, sub) or None
    if user is None:
        # support subject as email for simplicity
        user = get_user_by_email(db, sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post(
    "/signup",
    response_model=UserPublic,
    summary="Register a new user",
    description="Create a new user with email and password.",
)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, email=payload.email, password=payload.password, full_name=payload.full_name)
    return UserPublic(id=user.id, email=user.email, full_name=user.full_name, is_active=user.is_active)


@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="Authenticate with email and password to receive a JWT token.",
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(subject=user.email, expires_delta=access_token_expires)
    return Token(access_token=token)


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Get current user",
    description="Return information about the current authenticated user.",
)
def me(current_user=Depends(get_current_user)):
    return UserPublic(
        id=current_user.id, email=current_user.email, full_name=current_user.full_name, is_active=current_user.is_active
    )
