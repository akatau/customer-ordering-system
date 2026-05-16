"""
QA Sprint Week 7: Authentication Unit Tests
Tests for authentication, authorization, and token management
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt
import bcrypt

# Authentication Tests
class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_user_registration_success(self, db_session, valid_user_data):
        """Test successful user registration"""
        from app.services.auth_service import register_user
        
        user = register_user(db_session, **valid_user_data)
        
        assert user.email == valid_user_data["email"]
        assert user.first_name == valid_user_data["first_name"]
        assert user.is_active is True
        assert user.role == "customer"
        assert user.hashed_password != valid_user_data["password"]
    
    def test_user_registration_invalid_email(self, db_session, invalid_email_data):
        """Test registration with invalid email"""
        from app.services.auth_service import register_user
        from app.exceptions import ValidationError
        
        with pytest.raises(ValidationError):
            register_user(db_session, **invalid_email_data)
    
    def test_user_registration_duplicate_email(self, db_session, customer_user, valid_user_data):
        """Test registration with duplicate email"""
        from app.services.auth_service import register_user
        from app.exceptions import ValidationError
        
        valid_user_data["email"] = customer_user.email
        
        with pytest.raises(ValidationError):
            register_user(db_session, **valid_user_data)
    
    def test_user_registration_weak_password(self, db_session, weak_password_data):
        """Test registration with weak password"""
        from app.services.auth_service import register_user
        from app.exceptions import ValidationError
        
        with pytest.raises(ValidationError):
            register_user(db_session, **weak_password_data)


class TestUserLogin:
    """Test user login functionality"""
    
    def test_user_login_success(self, db_session, customer_user):
        """Test successful user login"""
        from app.services.auth_service import authenticate_user
        
        user = authenticate_user(db_session, customer_user.email, "hashed_password")
        
        assert user is not None
        assert user.email == customer_user.email
    
    def test_user_login_invalid_credentials(self, db_session, customer_user):
        """Test login with invalid credentials"""
        from app.services.auth_service import authenticate_user
        from app.exceptions import AuthenticationError
        
        with pytest.raises(AuthenticationError):
            authenticate_user(db_session, customer_user.email, "wrong_password")
    
    def test_user_login_nonexistent_user(self, db_session):
        """Test login with nonexistent user"""
        from app.services.auth_service import authenticate_user
        from app.exceptions import AuthenticationError
        
        with pytest.raises(AuthenticationError):
            authenticate_user(db_session, "nonexistent@example.com", "password")
    
    def test_user_login_inactive_user(self, db_session):
        """Test login with inactive user"""
        from app.models import User
        from app.services.auth_service import authenticate_user
        from app.exceptions import AuthenticationError
        
        user = User(
            email="inactive@example.com",
            hashed_password="hashed_password",
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()
        
        with pytest.raises(AuthenticationError):
            authenticate_user(db_session, user.email, "hashed_password")


class TestJWTTokens:
    """Test JWT token generation and validation"""
    
    def test_jwt_token_generation(self, customer_user):
        """Test JWT token generation"""
        from app.services.token_service import create_access_token
        
        token = create_access_token(customer_user.id, expires_in=30)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_jwt_token_validation(self, customer_user):
        """Test JWT token validation"""
        from app.services.token_service import create_access_token, verify_token
        
        token = create_access_token(customer_user.id, expires_in=30)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == str(customer_user.id)
    
    def test_jwt_token_expiration(self, customer_user):
        """Test JWT token expiration"""
        from app.services.token_service import create_access_token, verify_token
        from app.exceptions import TokenExpiredError
        
        # Create token with 0 expiration
        token = create_access_token(customer_user.id, expires_in=0)
        
        with pytest.raises(TokenExpiredError):
            verify_token(token)
    
    def test_jwt_invalid_token(self):
        """Test invalid JWT token"""
        from app.services.token_service import verify_token
        from app.exceptions import InvalidTokenError
        
        with pytest.raises(InvalidTokenError):
            verify_token("invalid.token.here")


class TestPasswordManagement:
    """Test password management"""
    
    def test_password_hashing(self, valid_user_data):
        """Test password hashing"""
        from app.services.auth_service import hash_password
        
        password = valid_user_data["password"]
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
    
    def test_password_verification(self, valid_user_data):
        """Test password verification"""
        from app.services.auth_service import hash_password, verify_password
        
        password = valid_user_data["password"]
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_password_reset_flow(self, db_session, customer_user):
        """Test password reset workflow"""
        from app.services.auth_service import request_password_reset, reset_password
        
        reset_token = request_password_reset(db_session, customer_user.email)
        assert reset_token is not None
        
        new_password = "NewSecurePassword123!"
        result = reset_password(db_session, reset_token, new_password)
        assert result is True


# Authorization Tests
class TestRoleBasedAccessControl:
    """Test role-based access control"""
    
    def test_admin_user_role(self, admin_user):
        """Test admin user role"""
        assert admin_user.role == "admin"
        assert admin_user.is_admin is True
    
    def test_customer_user_role(self, customer_user):
        """Test customer user role"""
        assert customer_user.role == "customer"
        assert customer_user.is_admin is False
    
    def test_support_user_role(self, db_session):
        """Test support staff role"""
        from app.models import User
        user = User(
            email="support@example.com",
            hashed_password="hashed",
            role="support",
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.role == "support"
    
    def test_role_permission_enforcement(self, admin_user, customer_user):
        """Test role-based permission enforcement"""
        from app.services.auth_service import check_permission
        
        # Admin should have admin permissions
        assert check_permission(admin_user, "admin:write") is True
        
        # Customer should not have admin permissions
        assert check_permission(customer_user, "admin:write") is False


class TestAccessControl:
    """Test access control enforcement"""
    
    def test_unauthenticated_user_blocked(self):
        """Test unauthenticated user access blocked"""
        from app.exceptions import UnauthorizedError
        from app.services.auth_service import require_auth
        
        with pytest.raises(UnauthorizedError):
            require_auth(None)
    
    def test_admin_endpoint_protection(self, db_session, customer_user):
        """Test admin endpoint protection"""
        from app.exceptions import ForbiddenError
        from app.services.auth_service import require_admin
        
        with pytest.raises(ForbiddenError):
            require_admin(customer_user)
    
    def test_authorized_admin_access(self, admin_user):
        """Test authorized admin access"""
        from app.services.auth_service import require_admin
        
        # Should not raise exception
        result = require_admin(admin_user)
        assert result is True
    
    def test_user_can_access_own_data(self, db_session, customer_user):
        """Test user can access own data"""
        from app.services.auth_service import check_user_access
        
        assert check_user_access(customer_user, customer_user.id) is True
    
    def test_user_cannot_access_other_data(self, db_session, customer_user):
        """Test user cannot access other user's data"""
        from app.services.auth_service import check_user_access
        from app.exceptions import ForbiddenError
        
        other_user_id = 999
        with pytest.raises(ForbiddenError):
            check_user_access(customer_user, other_user_id)


class TestSessionManagement:
    """Test session management"""
    
    def test_session_creation(self, db_session, customer_user):
        """Test session creation"""
        from app.models import Session as SessionModel
        
        session = SessionModel(
            user_id=customer_user.id,
            token="test_token",
            expires_at=datetime.utcnow() + timedelta(hours=24),
        )
        db_session.add(session)
        db_session.commit()
        
        assert session.user_id == customer_user.id
    
    def test_session_expiration(self, db_session, customer_user):
        """Test expired session detection"""
        from app.models import Session as SessionModel
        from app.services.auth_service import validate_session
        
        session = SessionModel(
            user_id=customer_user.id,
            token="test_token",
            expires_at=datetime.utcnow() - timedelta(hours=1),  # Expired
        )
        db_session.add(session)
        db_session.commit()
        
        assert validate_session(session) is False
    
    def test_session_invalidation(self, db_session, customer_user):
        """Test session invalidation (logout)"""
        from app.models import Session as SessionModel
        from app.services.auth_service import invalidate_session
        
        session = SessionModel(
            user_id=customer_user.id,
            token="test_token",
            expires_at=datetime.utcnow() + timedelta(hours=24),
            is_valid=True,
        )
        db_session.add(session)
        db_session.commit()
        
        invalidate_session(db_session, session.id)
        
        assert session.is_valid is False


class TestRefreshTokens:
    """Test refresh token functionality"""
    
    def test_refresh_token_generation(self, customer_user):
        """Test refresh token generation"""
        from app.services.token_service import create_refresh_token
        
        token = create_refresh_token(customer_user.id)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_refresh_token_validation(self, customer_user):
        """Test refresh token validation"""
        from app.services.token_service import create_refresh_token, verify_refresh_token
        
        token = create_refresh_token(customer_user.id)
        payload = verify_refresh_token(token)
        
        assert payload is not None
        assert payload["sub"] == str(customer_user.id)
    
    def test_token_refresh_flow(self, customer_user):
        """Test full token refresh flow"""
        from app.services.token_service import (
            create_access_token,
            create_refresh_token,
            refresh_access_token
        )
        
        refresh_token = create_refresh_token(customer_user.id)
        new_access_token = refresh_access_token(refresh_token)
        
        assert new_access_token is not None


# Security-specific tests
class TestPasswordSecurity:
    """Test password security measures"""
    
    def test_password_not_stored_plaintext(self, db_session, customer_user):
        """Test that passwords are not stored in plaintext"""
        assert customer_user.hashed_password != "password"
        assert customer_user.hashed_password != "plain_text_password"
    
    def test_password_salt_different(self, valid_user_data):
        """Test that password salts are different"""
        from app.services.auth_service import hash_password
        
        password = valid_user_data["password"]
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Same password should produce different hashes (due to different salt)
        assert hash1 != hash2
    
    def test_strong_password_requirement(self, db_session):
        """Test strong password requirement"""
        from app.services.auth_service import register_user
        from app.exceptions import ValidationError
        
        weak_passwords = [
            "123",  # Too short
            "password",  # No special chars
            "Pass123",  # No special chars
            "pass@123",  # No uppercase
        ]
        
        for weak_pass in weak_passwords:
            with pytest.raises(ValidationError):
                register_user(
                    db_session,
                    email=f"test_{weak_pass}@example.com",
                    password=weak_pass,
                )
