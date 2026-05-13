from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..api.deps import get_current_user, get_db
from ..schemas.profile import ChangePasswordRequest, UserProfileRead, UserProfileUpdate
from ..services.user_service import UserService

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserProfileRead)
def get_profile(user=Depends(get_current_user), db: Session = Depends(get_db)) -> UserProfileRead:
    return UserProfileRead.from_orm(user)


@router.put("/me", response_model=UserProfileRead)
def update_profile(payload: UserProfileUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> UserProfileRead:
    try:
        updated = UserService.update_profile(db, user, username=payload.username, full_name=payload.full_name)
        return UserProfileRead.from_orm(updated)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: ChangePasswordRequest, user=Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    try:
        UserService.change_password(db, user, payload.current_password, payload.new_password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
