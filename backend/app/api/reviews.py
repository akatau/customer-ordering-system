from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..api.deps import get_current_user, get_db
from ..schemas.review import ReviewCreate, ReviewRead
from ..services.review_service import ReviewService

router = APIRouter(tags=["Reviews"])


@router.get("/products/{product_id}", response_model=list[ReviewRead])
def list_reviews(product_id: str, db: Session = Depends(get_db)) -> list[ReviewRead]:
    return ReviewService.list_reviews(db, product_id)


@router.post("/products/{product_id}", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(product_id: str, payload: ReviewCreate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> ReviewRead:
    try:
        return ReviewService.create_review(db, user.id, product_id, payload.rating, payload.comment)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(review_id: str, payload: ReviewCreate, user=Depends(get_current_user), db: Session = Depends(get_db)) -> ReviewRead:
    try:
        return ReviewService.update_review(db, review_id, user.id, payload.rating, payload.comment)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    try:
        ReviewService.delete_review(db, review_id, user.id)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
