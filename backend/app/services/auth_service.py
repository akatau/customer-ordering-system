from sqlalchemy.orm import Session

from ..core.security import create_access_token, hash_password, verify_password
from ..models.user import User, UserRole


class AuthService:
    @staticmethod
    def register_user(db: Session, email: str, username: str, password: str, full_name: str | None = None) -> User:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise ValueError("Email already registered")

        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise ValueError("Username already taken")

        password_hash = hash_password(password)
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            password_hash=password_hash,
            role=UserRole.customer,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("Inactive user")
        return create_access_token(subject=str(user.id))
