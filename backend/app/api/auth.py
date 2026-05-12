from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.auth import Token, TokenPayload, UserLogin, UserRegister
from ..schemas.user import UserRead
from ..services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def register_user(payload: UserRegister, db: Session = Depends(get_db)) -> UserRead:
    try:
        user = AuthService.register_user(
            db,
            email=payload.email,
            username=payload.username,
            password=payload.password,
            full_name=payload.full_name,
        )
        return user
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=Token, tags=["Authentication"])
def login_user(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    try:
        access_token = AuthService.authenticate_user(db, payload.email, payload.password)
        return Token(access_token=access_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
