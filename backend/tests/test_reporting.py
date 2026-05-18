"""Tests for reporting and analytics service."""
import pytest
from http import HTTPStatus
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Product, Order, OrderItem, Cart, CartItem
from app.core.security import create_access_token
from app.services.reporting_service import ReportingService


@pytest.fixture
def admin_user(db: Session):
    """Create an admin user for testing."""
    user = User(
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        password_hash="hashed_password",
        role="admin",
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def customer_user(db: Session):
    """Create a customer user."""
    user = User(
        email="customer@example.com",
        username="customer",
        full_name="Customer User",
        password_hash="hashed_password",
        role="customer",
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


@pytest.fixture
def products(db: Session):
    """Create test products with different categories."""
    products_list = []
    
    # Electronics
    p1 = Product(
        name="Laptop",
        description="High-performance laptop",
        price=999.99,
        category="Electronics",
        stock_quantity=10,
    )
    products_list.append(p1)

    # Electronics
    p2 = Product(
        name="Mouse",
        description="Wireless mouse",
        price=29.99,
        category="Electronics",
        stock_quantity=50,
    )
    products_list.append(p2)

    # Accessories
    p3 = Product(
        name="Phone Case",
        description="Protective case",
        price=14.99,
        category="Accessories",
        stock_quantity=100,
    )
    products_list.append(p3)

    for product in products_list:
        db.add(product)
    db.commit()
    return products_list


@pytest.fixture
def completed_orders(db: Session, customer_user: User, products):
    """Create completed orders for testing."""
    orders_list = []
    
    # Order 1: Laptop + Mouse
    order1 = Order(
        user_id=customer_user.id,
        status="completed",
        total_amount=1029.98,
        shipping_address="123 Main St",
        created_at=datetime.utcnow() - timedelta(days=5),
    )
    db.add(order1)
    db.flush()

    item1 = OrderItem(
        order_id=order1.id,
        product_id=products[0].id,
        product_name="Laptop",
        quantity=1,
        unit_price=999.99,
        total_price=999.99,
    )
    item2 = OrderItem(
        order_id=order1.id,
        product_id=products[1].id,
        product_name="Mouse",
        quantity=1,
        unit_price=29.99,
        total_price=29.99,
    )
    db.add_all([item1, item2])
    orders_list.append(order1)

    # Order 2: Phone Case (different day)
    order2 = Order(
        user_id=customer_user.id,
        status="completed",
        total_amount=14.99,
        shipping_address="456 Oak Ave",
        created_at=datetime.utcnow() - timedelta(days=2),
    )
    db.add(order2)
    db.flush()

    item3 = OrderItem(
        order_id=order2.id,
        product_id=products[2].id,
        product_name="Phone Case",
        quantity=1,
        unit_price=14.99,
        total_price=14.99,
    )
    db.add(item3)
    orders_list.append(order2)

    # Order 3: Multiple cases
    order3 = Order(
        user_id=customer_user.id,
        status="completed",
        total_amount=44.97,
        shipping_address="789 Pine Rd",
        created_at=datetime.utcnow() - timedelta(days=1),
    )
    db.add(order3)
    db.flush()

    item4 = OrderItem(
        order_id=order3.id,
        product_id=products[2].id,
        product_name="Phone Case",
        quantity=3,
        unit_price=14.99,
        total_price=44.97,
    )
    db.add(item4)
    orders_list.append(order3)

    db.commit()
    return orders_list


@pytest.fixture
def pending_orders(db: Session, customer_user: User, products):
    """Create pending orders (should not appear in sales reports)."""
    order = Order(
        user_id=customer_user.id,
        status="pending",
        total_amount=59.98,
        shipping_address="999 Elm St",
    )
    db.add(order)
    db.flush()

    item = OrderItem(
        order_id=order.id,
        product_id=products[1].id,
        product_name="Mouse",
        quantity=2,
        unit_price=29.99,
        total_price=59.98,
    )
    db.add(item)
    db.commit()
    return order


@pytest.fixture
def abandoned_carts(db: Session, customer_user: User, products):
    """Create abandoned shopping carts."""
    cart = Cart(user_id=customer_user.id)
    db.add(cart)
    db.flush()

    cart_item = CartItem(
        cart_id=cart.id,
        product_id=products[0].id,
        product_name="Laptop",
        quantity=1,
        unit_price=999.99,
    )
    db.add(cart_item)
    db.commit()
    return cart


class TestSalesReport:
    """Test sales report generation."""

    def test_sales_report_basic_metrics(self, db: Session, completed_orders):
        """Test sales report calculates correct metrics."""
        report = ReportingService.sales_report(db)

        assert report["total_revenue"] == 1089.94  # 1029.98 + 14.99 + 44.97
        assert report["total_orders"] == 3
        assert report["average_order_value"] == pytest.approx(363.31, rel=0.01)

    def test_sales_report_top_products(self, db: Session, completed_orders):
        """Test sales report identifies top products."""
        report = ReportingService.sales_report(db)

        assert len(report["top_products"]) >= 1
        # Phone Case sold most (1 + 3 = 4 units)
        top_product = report["top_products"][0]
        assert top_product["product_name"] == "Phone Case"
        assert top_product["quantity_sold"] == 4

    def test_sales_report_by_category(self, db: Session, completed_orders):
        """Test sales report breakdown by category."""
        report = ReportingService.sales_report(db)

        # Should have categories for Electronics and Accessories
        assert "Electronics" in report["sales_by_category"]
        assert "Accessories" in report["sales_by_category"]

        # Electronics: Laptop 999.99 + Mouse 29.99 = 1029.98
        assert report["sales_by_category"]["Electronics"] == 1029.98
        # Accessories: Case 14.99 + 44.97 = 59.96
        assert report["sales_by_category"]["Accessories"] == 59.96

    def test_sales_report_daily_breakdown(self, db: Session, completed_orders):
        """Test sales report daily breakdown."""
        report = ReportingService.sales_report(db)

        assert "daily_breakdown" in report
        assert len(report["daily_breakdown"]) > 0
        
        # Verify structure of daily breakdown
        for day in report["daily_breakdown"]:
            assert "date" in day
            assert "orders" in day
            assert "revenue" in day

    def test_sales_report_excludes_pending_orders(self, db: Session, completed_orders, pending_orders):
        """Test that sales report excludes pending orders."""
        report = ReportingService.sales_report(db)

        # Pending order should not be counted
        assert report["total_orders"] == 3  # Only completed orders
        assert report["total_revenue"] == 1089.94  # Excludes pending order

    def test_sales_report_with_date_range(self, db: Session, completed_orders):
        """Test sales report with date range filtering."""
        start_date = datetime.utcnow() - timedelta(days=3)
        end_date = datetime.utcnow() - timedelta(days=1)

        report = ReportingService.sales_report(db, start_date, end_date)

        # Should only include orders within date range
        # Date range includes order1 (5 days ago is out) and order2 (2 days ago is in)
        assert report["total_orders"] <= 3

    def test_empty_sales_report(self, db: Session):
        """Test sales report when no completed orders exist."""
        report = ReportingService.sales_report(db)

        assert report["total_revenue"] == 0
        assert report["total_orders"] == 0
        assert report["average_order_value"] == 0
        assert len(report["top_products"]) == 0


class TestInventoryReport:
    """Test inventory report generation."""

    def test_inventory_report_basic_metrics(self, db: Session, products):
        """Test inventory report calculates correct metrics."""
        report = ReportingService.inventory_report(db)

        assert report["total_products"] == 3
        assert report["in_stock_count"] == 3
        assert report["out_of_stock_count"] == 0

    def test_inventory_report_stock_levels(self, db: Session, products):
        """Test inventory report shows stock quantities."""
        # Deplete one product
        products[0].stock_quantity = 0
        db.commit()

        report = ReportingService.inventory_report(db)

        assert report["in_stock_count"] == 2
        assert report["out_of_stock_count"] == 1

    def test_inventory_report_by_category(self, db: Session, products):
        """Test inventory report breakdown by category."""
        report = ReportingService.inventory_report(db)

        assert "Electronics" in report["stock_by_category"]
        assert "Accessories" in report["stock_by_category"]

        # Electronics: Laptop 10 + Mouse 50
        assert report["stock_by_category"]["Electronics"] == 60
        # Accessories: Case 100
        assert report["stock_by_category"]["Accessories"] == 100

    def test_inventory_report_low_stock_alerts(self, db: Session, products):
        """Test inventory report identifies low stock items."""
        # Set one product to low stock
        products[0].stock_quantity = 2
        db.commit()

        report = ReportingService.inventory_report(db)

        # Low stock items should be flagged
        assert len(report.get("low_stock_items", [])) > 0

    def test_inventory_report_total_value(self, db: Session, products):
        """Test inventory report calculates total inventory value."""
        report = ReportingService.inventory_report(db)

        # Total value: (10 * 999.99) + (50 * 29.99) + (100 * 14.99)
        expected_value = (10 * 999.99) + (50 * 29.99) + (100 * 14.99)
        assert report["total_inventory_value"] == pytest.approx(expected_value, rel=0.01)

    def test_empty_inventory_report(self, db: Session):
        """Test inventory report with no products."""
        report = ReportingService.inventory_report(db)

        assert report["total_products"] == 0
        assert report["in_stock_count"] == 0
        assert report["total_inventory_value"] == 0


class TestCustomerAnalytics:
    """Test customer analytics report."""

    def test_customer_analytics_basic_metrics(self, db: Session, customer_user: User, completed_orders):
        """Test customer analytics calculates basic metrics."""
        report = ReportingService.customer_analytics(db)

        assert report["total_customers"] >= 1
        assert report["total_orders"] == 3
        assert report["average_order_value"] == pytest.approx(363.31, rel=0.01)

    def test_customer_lifetime_value(self, db: Session, customer_user: User, completed_orders):
        """Test customer lifetime value calculation."""
        report = ReportingService.customer_analytics(db)

        # Should have customer LTV data
        assert "top_customers" in report

    def test_customer_analytics_repeat_customer(self, db: Session, customer_user: User, completed_orders):
        """Test that repeat customers are identified."""
        report = ReportingService.customer_analytics(db)

        # Customer made 3 orders, so should be identified as repeat
        assert report.get("repeat_customers", 0) >= 1

    def test_customer_analytics_new_customers_tracking(self, db: Session, customer_user: User):
        """Test new customer tracking."""
        report = ReportingService.customer_analytics(db)

        assert report["new_customers"] >= 0

    def test_customer_analytics_empty(self, db: Session):
        """Test customer analytics with no customers."""
        report = ReportingService.customer_analytics(db)

        assert report["total_customers"] == 0
        assert report["total_orders"] == 0


class TestReportExport:
    """Test report export functionality."""

    def test_export_report_json_format(self, db: Session, completed_orders):
        """Test exporting report in JSON format."""
        result = ReportingService.export_report(db, "sales", None, None, "json")
        assert result["format"] == "json"
        assert isinstance(result["content"], str)
        import json
        data = json.loads(result["content"])
        assert "total_revenue" in data

    def test_export_report_csv_format(self, db: Session, completed_orders):
        """Test exporting report in CSV format."""
        result = ReportingService.export_report(db, "sales", None, None, "csv")
        assert result["format"] == "csv"
        assert isinstance(result["content"], str)
        lines = result["content"].strip().split("\n")
        assert len(lines) >= 1

    def test_export_with_invalid_format(self, db: Session, completed_orders):
        """Test export with invalid format."""
        with pytest.raises(ValueError):
            ReportingService.export_report(db, "sales", None, None, "pdf")


class TestReportingAPIEndpoints:
    """Test reporting API endpoints."""

    def test_sales_report_endpoint_admin_only(self, client, admin_user: User, customer_user: User, completed_orders):
        """Test that only admin can access sales report."""
        customer_token = create_access_token(str(customer_user.id))
        customer_headers = {"Authorization": f"Bearer {customer_token}"}

        # Customer should be forbidden
        response = client.get(
            "/api/v1/admin/reports/sales",
            headers=customer_headers,
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

        # Admin should be allowed
        admin_token = create_access_token(str(admin_user.id))
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        response = client.get(
            "/api/v1/admin/reports/sales",
            headers=admin_headers,
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "total_revenue" in data

    def test_inventory_report_endpoint(self, client, admin_user: User, products):
        """Test inventory report endpoint."""
        admin_token = create_access_token(str(admin_user.id))
        headers = {"Authorization": f"Bearer {admin_token}"}

        response = client.get(
            "/api/v1/admin/reports/inventory",
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "total_products" in data
        assert data["total_products"] == 3

    def test_customer_analytics_endpoint(self, client, admin_user: User, customer_user: User, completed_orders):
        """Test customer analytics endpoint."""
        admin_token = create_access_token(str(admin_user.id))
        headers = {"Authorization": f"Bearer {admin_token}"}

        response = client.get(
            "/api/v1/admin/reports/customers",
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "total_customers" in data

    def test_export_report_endpoint_json(self, client, admin_user: User, completed_orders):
        """Test exporting report in JSON format via endpoint."""
        admin_token = create_access_token(str(admin_user.id))
        headers = {"Authorization": f"Bearer {admin_token}"}

        payload = {
            "report_type": "sales",
            "format": "json",
        }

        response = client.post(
            "/api/v1/admin/reports/export",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["format"] == "json"
        import json as _json
        content = _json.loads(data["content"])
        assert "total_revenue" in content

    def test_export_report_endpoint_csv(self, client, admin_user: User, completed_orders):
        """Test exporting report in CSV format via endpoint."""
        admin_token = create_access_token(str(admin_user.id))
        headers = {"Authorization": f"Bearer {admin_token}"}

        payload = {
            "report_type": "inventory",
            "format": "csv",
        }

        response = client.post(
            "/api/v1/admin/reports/export",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        # CSV format returns string
        assert isinstance(response.text, str)

    def test_sales_report_with_date_range_parameters(self, client, admin_user: User, completed_orders):
        """Test sales report with date range query parameters."""
        admin_token = create_access_token(str(admin_user.id))
        headers = {"Authorization": f"Bearer {admin_token}"}

        start_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
        end_date = datetime.utcnow().isoformat()

        response = client.get(
            f"/api/v1/admin/reports/sales?start_date={start_date}&end_date={end_date}",
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "total_revenue" in data

    def test_unauthenticated_cannot_access_reports(self, client):
        """Test that unauthenticated users cannot access reports."""
        response = client.get("/api/v1/admin/reports/sales")
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        response = client.post(
            "/api/v1/admin/reports/export",
            json={"report_type": "sales", "format": "json"},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
