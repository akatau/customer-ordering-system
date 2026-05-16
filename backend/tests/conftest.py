"""
Pytest configuration and shared fixtures for all tests
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models import Base, User, Product, Order, OrderItem
from app.services.auth_service import hash_password

@pytest.fixture(scope="function")
def db_engine():
    """Create an in-memory SQLite database for testing"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a fresh database session for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def admin_user(db_session):
    """Create a test admin user"""
    user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        hashed_password=hash_password("AdminPassword123!"),
        role="admin",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def customer_user(db_session):
    """Create a test customer user"""
    user = User(
        email="customer@example.com",
        first_name="John",
        last_name="Doe",
        hashed_password=hash_password("CustomerPassword123!"),
        role="customer",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def sample_product(db_session):
    """Create a single test product"""
    product = Product(
        name="Test Laptop",
        description="A portable computing device",
        price=Decimal("999.99"),
        stock=100,
        category="Electronics",
        is_active=True,
    )
    db_session.add(product)
    db_session.commit()
    return product

@pytest.fixture
def sample_products(db_session):
    """Create multiple test products"""
    products = [
        Product(
            name="Laptop Pro",
            description="High-performance laptop",
            price=Decimal("1299.99"),
            stock=50,
            category="Electronics",
            is_active=True,
        ),
        Product(
            name="Wireless Mouse",
            description="Portable wireless mouse",
            price=Decimal("29.99"),
            stock=200,
            category="Electronics",
            is_active=True,
        ),
        Product(
            name="USB-C Cable",
            description="High-speed USB-C cable",
            price=Decimal("14.99"),
            stock=500,
            category="Electronics",
            is_active=True,
        ),
    ]
    for product in products:
        db_session.add(product)
    db_session.commit()
    return products

@pytest.fixture
def sample_product_with_images(db_session):
    """Create a product with images"""
    product = Product(
        name="Product with Images",
        description="Test product",
        price=Decimal("100.00"),
        stock=10,
        category="Electronics",
        is_active=True,
    )
    product.images = [
        type('Image', (), {'url': 'https://example.com/image1.jpg'})(),
        type('Image', (), {'url': 'https://example.com/image2.jpg'})(),
    ]
    db_session.add(product)
    db_session.commit()
    return product

@pytest.fixture
def sample_product_with_reviews(db_session):
    """Create a product with reviews"""
    product = Product(
        name="Product with Reviews",
        description="Test product",
        price=Decimal("100.00"),
        stock=10,
        category="Electronics",
        is_active=True,
        average_rating=4.5,
    )
    product.reviews = [
        type('Review', (), {'rating': 5, 'comment': 'Great product!', 'user_id': 1})(),
        type('Review', (), {'rating': 4, 'comment': 'Good value', 'user_id': 2})(),
    ]
    db_session.add(product)
    db_session.commit()
    return product

@pytest.fixture
def order(db_session, customer_user, sample_product):
    """Create a test order"""
    order = Order(
        user_id=customer_user.id,
        status="pending",
        subtotal=Decimal("999.99"),
        tax=Decimal("79.99"),
        discount_amount=Decimal("0.00"),
        shipping_cost=Decimal("10.00"),
        total=Decimal("1089.98"),
        is_paid=False,
    )
    order_item = OrderItem(
        order=order,
        product_id=sample_product.id,
        quantity=1,
        price_at_purchase=sample_product.price,
    )
    db_session.add(order)
    db_session.add(order_item)
    db_session.commit()
    return order

@pytest.fixture
def pending_order(db_session, customer_user, sample_product):
    """Create a pending test order"""
    order = Order(
        user_id=customer_user.id,
        status="pending",
        subtotal=Decimal("999.99"),
        tax=Decimal("79.99"),
        discount_amount=Decimal("0.00"),
        shipping_cost=Decimal("10.00"),
        total=Decimal("1089.98"),
        is_paid=False,
    )
    order_item = OrderItem(
        order=order,
        product_id=sample_product.id,
        quantity=1,
        price_at_purchase=sample_product.price,
    )
    db_session.add(order)
    db_session.add(order_item)
    db_session.commit()
    return order

@pytest.fixture
def valid_user_data():
    """Valid user registration data"""
    return {
        "email": "newuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "SecurePassword123!",
    }

@pytest.fixture
def invalid_email_data():
    """Invalid email registration data"""
    return {
        "email": "invalid-email",
        "first_name": "John",
        "last_name": "Doe",
        "password": "SecurePassword123!",
    }

@pytest.fixture
def weak_password_data():
    """Weak password registration data"""
    return {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "weak",
    }
