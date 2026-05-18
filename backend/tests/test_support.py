"""Tests for support ticket system, refunds, and order modifications."""
import pytest
import uuid
from http import HTTPStatus
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.models import User, Product, Order, OrderItem, Ticket
from app.models.ticket import TicketStatus, TicketPriority, TicketCategory
from app.core.security import create_access_token
from app.services.support_service import (
    SupportService,
    RefundService,
    OrderModificationService,
)
from app.schemas.support import (
    TicketCreate,
    TicketUpdate,
    OrderModification,
    RefundRequest,
)


@pytest.fixture
def customer_user(db: Session):
    """Create a customer user for testing."""
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
def support_user(db: Session):
    """Create a support user for testing."""
    user = User(
        email="support@example.com",
        username="support",
        full_name="Support User",
        password_hash="hashed_password",
        role="support",
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


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
def test_order(db: Session, customer_user: User, test_product: Product):
    """Create a completed test order."""
    order = Order(
        user_id=customer_user.id,
        status="completed",
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
    db.commit()
    return order


@pytest.fixture
def pending_test_order(db: Session, customer_user: User, test_product: Product):
    """Create a pending test order for modification testing."""
    order = Order(
        user_id=customer_user.id,
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
    db.commit()
    return order


class TestSupportTicketCreation:
    """Test creating support tickets."""

    def test_customer_can_create_ticket(self, client, db: Session, customer_user: User, test_order: Order):
        """Test that customers can create support tickets."""
        token = create_access_token(str(customer_user.id))
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "subject": "Product arrived damaged",
            "description": "The product I received was damaged during shipping",
            "category": "shipping",
            "priority": "high",
            "order_id": str(test_order.id),
        }

        response = client.post(
            "/api/v1/support/tickets",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["subject"] == payload["subject"]
        assert data["category"] == payload["category"]
        assert data["priority"] == payload["priority"]
        assert data["status"] == "open"

    def test_create_ticket_without_order(self, client, customer_user: User):
        """Test creating a ticket without an associated order."""
        token = create_access_token(str(customer_user.id))
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "subject": "General inquiry",
            "description": "I have a question about products",
            "category": "product_question",
            "priority": "low",
        }

        response = client.post(
            "/api/v1/support/tickets",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["order_id"] is None

    def test_unauthenticated_cannot_create_ticket(self, client):
        """Test that unauthenticated users cannot create tickets."""
        payload = {
            "subject": "Test ticket",
            "description": "Test description",
            "category": "other",
            "priority": "low",
        }

        response = client.post("/api/v1/support/tickets", json=payload)
        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestSupportTicketListingAndAccess:
    """Test listing and accessing support tickets."""

    def test_customer_sees_only_own_tickets(self, db: Session, customer_user: User, support_user: User):
        """Test that customers only see their own tickets."""
        # Create ticket for customer
        ticket1 = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="My issue",
            description="My problem",
            category=TicketCategory.ORDER_ISSUE,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket1)
        db.commit()

        # Create another ticket for different user
        ticket2 = Ticket(
            id=str(uuid.uuid4()),
            user_id=support_user.id,
            subject="Support issue",
            description="Support problem",
            category=TicketCategory.REFUND,
            priority=TicketPriority.HIGH,
        )
        db.add(ticket2)
        db.commit()

        # Query as customer
        tickets, total = SupportService.list_tickets(
            db,
            user_id=customer_user.id,
        )

        assert len(tickets) == 1
        assert tickets[0].id == ticket1.id
        assert total == 1

    def test_support_can_list_all_tickets(self, db: Session, customer_user: User, support_user: User):
        """Test that support users can see all tickets."""
        # Create multiple tickets
        ticket1 = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Customer issue",
            description="Problem 1",
            category=TicketCategory.ORDER_ISSUE,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket1)

        ticket2 = Ticket(
            id=str(uuid.uuid4()),
            user_id=support_user.id,
            subject="Another issue",
            description="Problem 2",
            category=TicketCategory.SHIPPING,
            priority=TicketPriority.HIGH,
        )
        db.add(ticket2)
        db.commit()

        # List without user_id filter (support view)
        tickets, total = SupportService.list_tickets(db)

        assert len(tickets) == 2
        assert total == 2

    def test_list_tickets_with_status_filter(self, db: Session, customer_user: User):
        """Test listing tickets filtered by status."""
        # Create tickets with different statuses
        open_ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Open ticket",
            description="Still open",
            category=TicketCategory.OTHER,
            priority=TicketPriority.LOW,
            status=TicketStatus.OPEN,
        )
        db.add(open_ticket)

        resolved_ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Resolved ticket",
            description="Already resolved",
            category=TicketCategory.OTHER,
            priority=TicketPriority.LOW,
            status=TicketStatus.RESOLVED,
        )
        db.add(resolved_ticket)
        db.commit()

        # Filter by open status
        open_tickets, total = SupportService.list_tickets(
            db,
            status=TicketStatus.OPEN,
        )

        assert len(open_tickets) == 1
        assert open_tickets[0].status == TicketStatus.OPEN
        assert total == 1


class TestSupportTicketUpdates:
    """Test updating support tickets."""

    def test_update_ticket_status(self, db: Session, customer_user: User):
        """Test updating ticket status and resolved_at timestamp."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test ticket",
            description="Test",
            category=TicketCategory.OTHER,
            priority=TicketPriority.LOW,
        )
        db.add(ticket)
        db.commit()

        # Update to resolved
        update_data = TicketUpdate(status=TicketStatus.RESOLVED)
        updated = SupportService.update_ticket(db, ticket.id, update_data)

        assert updated.status == TicketStatus.RESOLVED
        assert updated.resolved_at is not None

    def test_update_ticket_priority(self, db: Session, customer_user: User):
        """Test updating ticket priority."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test ticket",
            description="Test",
            category=TicketCategory.ORDER_ISSUE,
            priority=TicketPriority.LOW,
        )
        db.add(ticket)
        db.commit()

        update_data = TicketUpdate(priority=TicketPriority.CRITICAL)
        updated = SupportService.update_ticket(db, ticket.id, update_data)

        assert updated.priority == TicketPriority.CRITICAL

    def test_add_internal_note(self, db: Session, customer_user: User):
        """Test adding internal notes to tickets."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test ticket",
            description="Test",
            category=TicketCategory.OTHER,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket)
        db.commit()

        # Add note
        SupportService.add_note(db, ticket.id, "Investigating issue")
        db.refresh(ticket)

        assert "Investigating issue" in ticket.internal_notes
        assert ticket.internal_notes.startswith("[")

    def test_add_multiple_notes(self, db: Session, customer_user: User):
        """Test adding multiple notes to a ticket."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test ticket",
            description="Test",
            category=TicketCategory.REFUND,
            priority=TicketPriority.HIGH,
        )
        db.add(ticket)
        db.commit()

        # Add multiple notes
        SupportService.add_note(db, ticket.id, "First note")
        SupportService.add_note(db, ticket.id, "Second note")
        db.refresh(ticket)

        assert "First note" in ticket.internal_notes
        assert "Second note" in ticket.internal_notes

    def test_escalate_ticket(self, db: Session, customer_user: User, admin_user: User):
        """Test escalating ticket to admin."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test ticket",
            description="Test",
            category=TicketCategory.OTHER,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket)
        db.commit()

        # Escalate
        escalated = SupportService.escalate_ticket(db, ticket.id, admin_user.id)

        assert escalated.assigned_to == admin_user.id
        assert escalated.priority == TicketPriority.HIGH


class TestRefundProcessing:
    """Test refund service."""

    def test_process_refund_for_completed_order(self, db: Session, test_order: Order):
        """Test processing refund for a completed order."""
        refund_result = RefundService.process_refund(
            db,
            order_id=test_order.id,
            reason="Damaged item",
            amount=test_order.total_amount,
        )

        assert "refund_id" in refund_result
        assert refund_result["status"] == "completed"
        
        # Check order status updated to cancelled
        db.refresh(test_order)
        assert test_order.status == "cancelled"

    def test_refund_non_existent_order(self, db: Session):
        """Test refunding a non-existent order raises error."""
        with pytest.raises(ValueError, match="not found"):
            RefundService.process_refund(
                db,
                order_id="non-existent-id",
                reason="Test",
            )

    def test_refund_cancelled_order_fails(self, db: Session, customer_user: User):
        """Test refunding a cancelled order fails."""
        order = Order(
            user_id=customer_user.id,
            status="cancelled",
            total_amount=29.99,
            shipping_address="123 Test St",
        )
        db.add(order)
        db.commit()

        with pytest.raises(ValueError, match="Cannot refund"):
            RefundService.process_refund(
                db,
                order_id=order.id,
                reason="Changed mind",
            )


class TestOrderModification:
    """Test order modification service."""

    def test_add_item_to_order(self, db: Session, pending_test_order: Order, test_product: Product):
        """Test adding an item to an order."""
        # Create another product
        new_product = Product(
            name="New Product",
            description="Another product",
            price=19.99,
            category="Test",
            stock_quantity=50,
        )
        db.add(new_product)
        db.commit()

        initial_total = pending_test_order.total_amount
        modification = OrderModification(
            action="add_item",
            product_id=new_product.id,
            quantity=1,
            reason="Customer requested additional item",
        )

        result = OrderModificationService.modify_order(
            db,
            pending_test_order.id,
            modification,
            "support-user-id",
        )

        assert result["status"] == "success"
        db.refresh(pending_test_order)
        assert pending_test_order.total_amount == Decimal("29.99") + Decimal("19.99")
        assert len(pending_test_order.items) == 2

    def test_remove_item_from_order(self, db: Session, pending_test_order: Order):
        """Test removing an item from an order."""
        # Get the order item
        order_item = pending_test_order.items[0]
        initial_total = pending_test_order.total_amount

        modification = OrderModification(
            action="remove_item",
            product_id=order_item.product_id,
            reason="Customer requested item removal",
        )

        result = OrderModificationService.modify_order(
            db,
            pending_test_order.id,
            modification,
            "support-user-id",
        )

        assert result["status"] == "success"
        db.refresh(pending_test_order)
        assert pending_test_order.total_amount == Decimal("0")
        assert len(pending_test_order.items) == 0

    def test_change_address(self, db: Session, pending_test_order: Order):
        """Test changing order shipping address."""
        new_address = "456 New Street, New City, NY 10001"
        modification = OrderModification(
            action="change_address",
            shipping_address={"street": new_address},
            reason="Customer requested address change",
        )

        result = OrderModificationService.modify_order(
            db,
            pending_test_order.id,
            modification,
            "support-user-id",
        )

        assert result["status"] == "success"
        db.refresh(pending_test_order)
        assert new_address in pending_test_order.shipping_address

    def test_add_item_insufficient_stock(self, db: Session, pending_test_order: Order):
        """Test adding item fails if insufficient stock."""
        # Create product with no stock
        no_stock_product = Product(
            name="Out of Stock",
            description="No stock",
            price=39.99,
            category="Test",
            stock_quantity=0,
        )
        db.add(no_stock_product)
        db.commit()

        modification = OrderModification(
            action="add_item",
            product_id=no_stock_product.id,
            quantity=1,
            reason="Customer wants to add item",
        )

        with pytest.raises(ValueError, match="Not enough stock"):
            OrderModificationService.modify_order(
                db,
                pending_test_order.id,
                modification,
                "support-user-id",
            )


class TestSupportAPIEndpoints:
    """Test support API endpoints with HTTP requests."""

    def test_create_ticket_via_api(self, client, customer_user: User, test_order: Order):
        """Test creating ticket through API endpoint."""
        token = create_access_token(str(customer_user.id))
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "subject": "Issue with order",
            "description": "Product does not match description",
            "category": "product_question",
            "priority": "high",
            "order_id": str(test_order.id),
        }

        response = client.post(
            "/api/v1/support/tickets",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        ticket_id = data["id"]

        # Verify can retrieve ticket
        get_response = client.get(
            f"/api/v1/support/tickets/{ticket_id}",
            headers=headers,
        )
        assert get_response.status_code == HTTPStatus.OK

    def test_list_tickets_via_api(self, client, customer_user: User, db: Session):
        """Test listing tickets through API endpoint."""
        token = create_access_token(str(customer_user.id))
        headers = {"Authorization": f"Bearer {token}"}

        # Create a ticket
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test",
            description="Test ticket",
            category=TicketCategory.ORDER_ISSUE,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket)
        db.commit()

        response = client.get(
            "/api/v1/support/tickets",
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["total"] >= 1
        assert len(data["items"]) >= 1

    def test_only_support_can_modify_ticket(self, client, customer_user: User, support_user: User, db: Session):
        """Test that only support staff can modify tickets."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test",
            description="Test ticket",
            category=TicketCategory.OTHER,
            priority=TicketPriority.LOW,
        )
        db.add(ticket)
        db.commit()

        # Customer tries to update ticket
        customer_token = create_access_token(str(customer_user.id))
        customer_headers = {"Authorization": f"Bearer {customer_token}"}

        payload = {"status": "closed"}
        response = client.put(
            f"/api/v1/support/tickets/{ticket.id}",
            json=payload,
            headers=customer_headers,
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

        # Support staff can update
        support_token = create_access_token(str(support_user.id))
        support_headers = {"Authorization": f"Bearer {support_token}"}

        response = client.put(
            f"/api/v1/support/tickets/{ticket.id}",
            json=payload,
            headers=support_headers,
        )
        assert response.status_code == HTTPStatus.OK

    def test_add_note_to_ticket_via_api(self, client, support_user: User, customer_user: User, db: Session):
        """Test adding note to ticket via API."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=customer_user.id,
            subject="Test",
            description="Test ticket",
            category=TicketCategory.ORDER_ISSUE,
            priority=TicketPriority.MEDIUM,
        )
        db.add(ticket)
        db.commit()

        support_token = create_access_token(str(support_user.id))
        headers = {"Authorization": f"Bearer {support_token}"}

        payload = {"note": "Customer contacted via email"}
        response = client.post(
            f"/api/v1/support/tickets/{ticket.id}/notes",
            json=payload,
            headers=headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "Customer contacted via email" in data["internal_notes"]
