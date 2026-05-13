from sqlalchemy.orm import Session

from ..core.security import hash_password, verify_password
from ..models.user import User


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_profile(db: Session, user: User, username: str | None = None, full_name: str | None = None) -> User:
        if username and username != user.username:
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                raise ValueError("Username already taken")
            user.username = username

        if full_name is not None:
            user.full_name = full_name

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user: User, current_password: str, new_password: str) -> None:
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        user.password_hash = hash_password(new_password)
        db.commit()
