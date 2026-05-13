import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Product, Order, AdminLog
from app.core.security import create_access_token


@pytest.fixture
def admin_user(db: Session):
    """Create an admin user for testing."""
    admin = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        password_hash="hashed_password",
        role="admin",
        is_active=True,
    )
    db.add(admin)
    db.flush()
    return admin


@pytest.fixture
def support_user(db: Session):
    """Create a support user for testing."""
    support = User(
        email="support@example.com",
        username="support",
        full_name="Support User",
        password_hash="hashed_password",
        role="support",
        is_active=True,
    )
    db.add(support)
    db.flush()
    return support


@pytest.fixture
def regular_user(db: Session):
    """Create a regular user for testing."""
    user = User(
        email="user@example.com",
        username="user",
        full_name="Regular User",
        password_hash="hashed_password",
        role="customer",
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def test_product(db: Session):
    """Create a test product."""
    product = Product(
        name="Test Product",
        description="A test product",
        price=29.99,
        category="Test",
        stock_quantity=100,
    )
    db.add(product)
    db.flush()
    return product


@pytest.fixture
def test_order(db: Session, regular_user: User, test_product: Product):
    """Create a test order."""
    from app.models import OrderItem

    order = Order(
        user_id=regular_user.id,
        status="pending",
        total_amount=29.99,
        shipping_address="123 Test St",
    )
    db.add(order)
    db.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        product_name=test_product.name,
        quantity=1,
        unit_price=29.99,
        total_price=29.99,
    )
    db.add(order_item)
    db.flush()

    return order


def get_auth_header(user: User):
    """Get authorization header for a user."""
    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}


class TestAdminAuthorization:
    def test_admin_access_granted(self, client: TestClient, admin_user: User):
        """Test that admin can access admin endpoints."""
        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/users", headers=headers)
        assert response.status_code == 200

    def test_support_access_granted(self, client: TestClient, support_user: User):
        """Test that support can access admin endpoints."""
        headers = get_auth_header(support_user)
        response = client.get("/api/v1/admin/orders", headers=headers)
        assert response.status_code == 200

    def test_regular_user_access_denied(self, client: TestClient, regular_user: User):
        """Test that regular users cannot access admin endpoints."""
        headers = get_auth_header(regular_user)
        response = client.get("/api/v1/admin/users", headers=headers)
        assert response.status_code == 403

    def test_unauthenticated_access_denied(self, client: TestClient):
        """Test that unauthenticated users cannot access admin endpoints."""
        response = client.get("/api/v1/admin/users")
        assert response.status_code == 401


class TestProductManagement:
    def test_create_product_admin_only(self, client: TestClient, admin_user: User):
        """Test creating a product (admin only)."""
        headers = get_auth_header(admin_user)
        product_data = {
            "name": "New Product",
            "description": "A new product",
            "price": 19.99,
            "category": "Electronics",
            "stock_quantity": 50,
        }
        response = client.post("/api/v1/admin/products", json=product_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "product_id" in data
        assert data["message"] == "Product created successfully"

    def test_update_product(self, client: TestClient, admin_user: User, test_product: Product):
        """Test updating a product."""
        headers = get_auth_header(admin_user)
        update_data = {"price": 39.99, "stock_quantity": 75}
        response = client.put(
            f"/api/v1/admin/products/{test_product.id}",
            json=update_data,
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Product updated successfully"

    def test_delete_product(self, client: TestClient, admin_user: User, test_product: Product):
        """Test deleting a product."""
        headers = get_auth_header(admin_user)
        response = client.delete(f"/api/v1/admin/products/{test_product.id}", headers=headers)
        assert response.status_code == 204

    def test_delete_ordered_product_fails(self, client: TestClient, admin_user: User, test_order: Order, db: Session):
        """Test that deleting a product that's been ordered fails."""
        from app.models import OrderItem

        # Get the product ID from the order
        order_item = db.query(OrderItem).filter(OrderItem.order_id == test_order.id).first()
        product_id = order_item.product_id

        headers = get_auth_header(admin_user)
        response = client.delete(f"/api/v1/admin/products/{product_id}", headers=headers)
        assert response.status_code == 400
        assert "Cannot delete product that has been ordered" in response.json()["detail"]

    def test_export_products(self, client: TestClient, admin_user: User):
        """Test exporting products to CSV."""
        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/products/export", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "export_url" in data
        assert data["message"] == "Products exported successfully"


class TestUserManagement:
    def test_get_users(self, client: TestClient, admin_user: User, regular_user: User):
        """Test getting list of users."""
        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/users", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert len(data["users"]) >= 2  # At least admin and regular user

    def test_update_user(self, client: TestClient, admin_user: User, regular_user: User):
        """Test updating a user."""
        headers = get_auth_header(admin_user)
        update_data = {"full_name": "Updated Name", "role": "support"}
        response = client.put(
            f"/api/v1/admin/users/{regular_user.id}",
            json=update_data,
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["role"] == "support"

    def test_deactivate_user(self, client: TestClient, admin_user: User, regular_user: User):
        """Test deactivating a user."""
        headers = get_auth_header(admin_user)
        response = client.delete(f"/api/v1/admin/users/{regular_user.id}", headers=headers)
        assert response.status_code == 204

    def test_deactivate_admin_fails(self, client: TestClient, admin_user: User):
        """Test that deactivating an admin user fails."""
        headers = get_auth_header(admin_user)
        response = client.delete(f"/api/v1/admin/users/{admin_user.id}", headers=headers)
        assert response.status_code == 400
        assert "Cannot deactivate admin user" in response.json()["detail"]


class TestOrderManagement:
    def test_get_orders(self, client: TestClient, admin_user: User, test_order: Order):
        """Test getting list of orders."""
        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/orders", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert len(data["orders"]) >= 1

    def test_update_order(self, client: TestClient, admin_user: User, test_order: Order):
        """Test updating an order."""
        headers = get_auth_header(admin_user)
        update_data = {"status": "completed"}
        response = client.put(
            f"/api/v1/admin/orders/{test_order.id}",
            json=update_data,
            headers=headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    def test_generate_invoice(self, client: TestClient, admin_user: User, test_order: Order):
        """Test generating an invoice."""
        headers = get_auth_header(admin_user)
        response = client.get(f"/api/v1/admin/orders/{test_order.id}/invoice", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "invoice_url" in data
        assert data["message"] == "Invoice generated successfully"


class TestActivityLogs:
    def test_get_activity_logs(self, client: TestClient, admin_user: User, db: Session):
        """Test getting activity logs."""
        # Create some log entries
        log1 = AdminLog(
            admin_user_id=admin_user.id,
            action="create_product",
            resource_type="product",
            resource_id="test-id",
            details={"name": "Test Product"},
        )
        db.add(log1)
        db.commit()

        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/activity-logs", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert len(data["logs"]) >= 1

    def test_filter_activity_logs(self, client: TestClient, admin_user: User, db: Session):
        """Test filtering activity logs."""
        log1 = AdminLog(
            admin_user_id=admin_user.id,
            action="create_product",
            resource_type="product",
            resource_id="test-id",
        )
        log2 = AdminLog(
            admin_user_id=admin_user.id,
            action="update_user",
            resource_type="user",
            resource_id="user-id",
        )
        db.add(log1)
        db.add(log2)
        db.commit()

        headers = get_auth_header(admin_user)
        response = client.get("/api/v1/admin/activity-logs?action=create_product", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["logs"]) == 1
        assert data["logs"][0]["action"] == "create_product"
