from sqlalchemy.orm import Session

from ..models.order import Order, OrderItem
from ..models.product import Product
from ..models.review import Review


class ReviewService:
    @staticmethod
    def list_reviews(db: Session, product_id: str) -> list[Review]:
        return db.query(Review).filter(Review.product_id == product_id).all()

    @staticmethod
    def create_review(db: Session, user_id: str, product_id: str, rating: int, comment: str | None) -> Review:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise ValueError("Product not found")

        purchased = (
            db.query(OrderItem)
            .join(Order)
            .filter(OrderItem.product_id == product_id, Order.user_id == user_id)
            .first()
        )
        if purchased is None:
            raise ValueError("Product must be purchased before reviewing")

        review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_review(db: Session, review_id: str) -> Review | None:
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def update_review(db: Session, review_id: str, user_id: str, rating: int, comment: str | None) -> Review:
        review = ReviewService.get_review(db, review_id)
        if review is None:
            raise ValueError("Review not found")
        if review.user_id != user_id:
            raise PermissionError("Unauthorized")

        review.rating = rating
        review.comment = comment
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete_review(db: Session, review_id: str, user_id: str) -> None:
        review = ReviewService.get_review(db, review_id)
        if review is None:
            raise ValueError("Review not found")
        if review.user_id != user_id:
            raise PermissionError("Unauthorized")

        db.delete(review)
        db.commit()
