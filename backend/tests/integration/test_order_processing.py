"""
QA Sprint Week 7: Order Processing Integration Tests
Tests for order creation, management, and fulfillment
"""

import pytest
from datetime import datetime
from decimal import Decimal

class TestOrderCreation:
    """Test order creation"""
    
    def test_create_order_success(self, db_session, customer_user, sample_products):
        """Test successful order creation"""
        from app.services.order_service import create_order
        
        items = [
            {"product_id": sample_products[0].id, "quantity": 2},
            {"product_id": sample_products[1].id, "quantity": 1},
        ]
        
        order = create_order(db_session, customer_user.id, items)
        
        assert order is not None
        assert order.user_id == customer_user.id
        assert len(order.items) == 2
    
    def test_create_order_empty_items(self, db_session, customer_user):
        """Test order creation with empty items"""
        from app.services.order_service import create_order
        from app.exceptions import ValidationError
        
        with pytest.raises(ValidationError):
            create_order(db_session, customer_user.id, [])
    
    def test_create_order_invalid_product(self, db_session, customer_user):
        """Test order creation with invalid product"""
        from app.services.order_service import create_order
        from app.exceptions import NotFoundError
        
        items = [{"product_id": 99999, "quantity": 1}]
        
        with pytest.raises(NotFoundError):
            create_order(db_session, customer_user.id, items)
    
    def test_create_order_insufficient_stock(self, db_session, customer_user, sample_product):
        """Test order creation with insufficient stock"""
        from app.services.order_service import create_order
        from app.exceptions import InsufficientStockError
        
        items = [{"product_id": sample_product.id, "quantity": 1000}]
        
        with pytest.raises(InsufficientStockError):
            create_order(db_session, customer_user.id, items)


class TestOrderTotals:
    """Test order total calculations"""
    
    def test_order_subtotal_calculation(self, db_session, customer_user, sample_products):
        """Test order subtotal calculation"""
        from app.services.order_service import create_order
        
        items = [
            {"product_id": sample_products[0].id, "quantity": 2},  # $100 * 2
            {"product_id": sample_products[1].id, "quantity": 1},  # $200 * 1
        ]
        
        order = create_order(db_session, customer_user.id, items)
        
        expected_subtotal = (sample_products[0].price * 2) + sample_products[1].price
        assert order.subtotal == expected_subtotal
    
    def test_order_tax_calculation(self, db_session, customer_user, sample_products):
        """Test order tax calculation"""
        from app.services.order_service import create_order
        
        items = [{"product_id": sample_products[0].id, "quantity": 1}]
        
        order = create_order(db_session, customer_user.id, items)
        
        expected_tax = order.subtotal * Decimal("0.08")  # 8% tax rate
        assert order.tax == expected_tax
    
    def test_order_discount_application(self, db_session, customer_user, sample_products):
        """Test order discount application"""
        from app.services.order_service import create_order, apply_discount
        
        items = [{"product_id": sample_products[0].id, "quantity": 1}]
        order = create_order(db_session, customer_user.id, items)
        
        coupon = "SAVE10"
        apply_discount(db_session, order.id, coupon)
        
        expected_discount = order.subtotal * Decimal("0.10")
        assert order.discount_amount == expected_discount
    
    def test_order_total_calculation(self, db_session, customer_user, sample_products):
        """Test order total calculation"""
        from app.services.order_service import create_order
        
        items = [{"product_id": sample_products[0].id, "quantity": 1}]
        order = create_order(db_session, customer_user.id, items)
        
        expected_total = order.subtotal + order.tax - order.discount_amount
        assert order.total == expected_total
    
    def test_order_shipping_cost(self, db_session, customer_user, sample_products):
        """Test order shipping cost"""
        from app.services.order_service import create_order
        
        items = [{"product_id": sample_products[0].id, "quantity": 1}]
        order = create_order(db_session, customer_user.id, items)
        
        assert order.shipping_cost >= Decimal("0")


class TestOrderStatus:
    """Test order status management"""
    
    def test_order_initial_status(self, db_session, customer_user, sample_product):
        """Test order has correct initial status"""
        from app.services.order_service import create_order
        
        items = [{"product_id": sample_product.id, "quantity": 1}]
        order = create_order(db_session, customer_user.id, items)
        
        assert order.status == "pending"
    
    def test_order_status_transitions(self, db_session, order):
        """Test valid order status transitions"""
        from app.services.order_service import update_order_status
        
        # Pending -> Confirmed
        update_order_status(db_session, order.id, "confirmed")
        assert order.status == "confirmed"
        
        # Confirmed -> Shipped
        update_order_status(db_session, order.id, "shipped")
        assert order.status == "shipped"
        
        # Shipped -> Delivered
        update_order_status(db_session, order.id, "delivered")
        assert order.status == "delivered"
    
    def test_order_invalid_status_transition(self, db_session, order):
        """Test invalid order status transition"""
        from app.services.order_service import update_order_status
        from app.exceptions import ValidationError
        
        with pytest.raises(ValidationError):
            # Can't go from pending to delivered
            update_order_status(db_session, order.id, "delivered")
    
    def test_order_cancellation(self, db_session, order):
        """Test order cancellation"""
        from app.services.order_service import cancel_order
        
        cancel_order(db_session, order.id)
        
        assert order.status == "cancelled"
        assert order.cancelled_at is not None


class TestOrderRetrieval:
    """Test order retrieval"""
    
    def test_get_order_by_id(self, db_session, order):
        """Test retrieving order by ID"""
        from app.services.order_service import get_order
        
        retrieved = get_order(db_session, order.id)
        
        assert retrieved.id == order.id
    
    def test_get_user_orders(self, db_session, customer_user):
        """Test retrieving user's orders"""
        from app.services.order_service import get_user_orders
        
        orders = get_user_orders(db_session, customer_user.id)
        
        assert len(orders) > 0
        assert all(o.user_id == customer_user.id for o in orders)
    
    def test_get_order_not_found(self, db_session):
        """Test order not found"""
        from app.services.order_service import get_order
        from app.exceptions import NotFoundError
        
        with pytest.raises(NotFoundError):
            get_order(db_session, 99999)


class TestOrderPayment:
    """Test order payment processing"""
    
    def test_mark_order_as_paid(self, db_session, order):
        """Test marking order as paid"""
        from app.services.order_service import mark_order_paid
        
        mark_order_paid(db_session, order.id)
        
        assert order.is_paid is True
        assert order.paid_at is not None
    
    def test_process_payment_success(self, db_session, order):
        """Test successful payment processing"""
        from app.services.payment_service import process_payment
        
        result = process_payment(
            db_session,
            order.id,
            "4111111111111111",  # Test card
            "12/25",
            "123"
        )
        
        assert result.success is True
        assert order.is_paid is True
    
    def test_process_payment_declined(self, db_session, order):
        """Test declined payment"""
        from app.services.payment_service import process_payment
        from app.exceptions import PaymentError
        
        with pytest.raises(PaymentError):
            process_payment(
                db_session,
                order.id,
                "4000000000000002",  # Declined test card
                "12/25",
                "123"
            )
    
    def test_refund_order(self, db_session, order):
        """Test order refund"""
        from app.services.payment_service import refund_payment
        from app.services.order_service import mark_order_paid
        
        mark_order_paid(db_session, order.id)
        result = refund_payment(db_session, order.id)
        
        assert result.success is True
        assert order.is_refunded is True


class TestOrderItems:
    """Test order items"""
    
    def test_order_items_price_locked(self, db_session, order):
        """Test order item prices are locked"""
        for item in order.items:
            # Prices should be captured at order time
            assert item.price_at_purchase is not None
    
    def test_order_item_quantity_matches_order(self, db_session, customer_user, sample_product):
        """Test order item quantities"""
        from app.services.order_service import create_order
        
        items = [{"product_id": sample_product.id, "quantity": 5}]
        order = create_order(db_session, customer_user.id, items)
        
        assert order.items[0].quantity == 5


class TestOrderTracking:
    """Test order tracking"""
    
    def test_order_tracking_number(self, db_session, order):
        """Test order has tracking number after shipment"""
        from app.services.order_service import update_order_status
        
        update_order_status(db_session, order.id, "shipped")
        
        assert order.tracking_number is not None
    
    def test_track_order_by_number(self, db_session, order):
        """Test tracking order by tracking number"""
        from app.services.order_service import track_order
        from app.services.order_service import update_order_status
        
        update_order_status(db_session, order.id, "shipped")
        tracked = track_order(db_session, order.tracking_number)
        
        assert tracked.id == order.id


class TestOrderNotifications:
    """Test order notifications"""
    
    def test_order_confirmation_email_sent(self, db_session, customer_user, sample_product):
        """Test order confirmation email sent"""
        from app.services.order_service import create_order
        from app.services.notification_service import get_notification
        
        items = [{"product_id": sample_product.id, "quantity": 1}]
        order = create_order(db_session, customer_user.id, items)
        
        notification = get_notification(
            db_session,
            order.id,
            "order_confirmed"
        )
        
        assert notification is not None
        assert notification.recipient == customer_user.email
    
    def test_order_status_update_notification(self, db_session, customer_user, order):
        """Test order status update notification"""
        from app.services.order_service import update_order_status
        from app.services.notification_service import get_notification
        
        update_order_status(db_session, order.id, "confirmed")
        
        notification = get_notification(
            db_session,
            order.id,
            "order_status_updated"
        )
        
        assert notification is not None


class TestOrderModification:
    """Test order modification"""
    
    def test_add_item_to_pending_order(self, db_session, pending_order, sample_product):
        """Test adding item to pending order"""
        from app.services.order_service import add_item_to_order
        
        original_count = len(pending_order.items)
        add_item_to_order(db_session, pending_order.id, sample_product.id, 1)
        
        assert len(pending_order.items) == original_count + 1
    
    def test_cannot_modify_confirmed_order(self, db_session, order):
        """Test cannot modify confirmed order"""
        from app.services.order_service import update_order_status, add_item_to_order
        from app.exceptions import ValidationError
        
        update_order_status(db_session, order.id, "confirmed")
        
        with pytest.raises(ValidationError):
            add_item_to_order(db_session, order.id, 1, 1)
    
    def test_update_order_quantity(self, db_session, pending_order):
        """Test updating item quantity in pending order"""
        from app.services.order_service import update_item_quantity
        
        item = pending_order.items[0]
        original_qty = item.quantity
        
        update_item_quantity(db_session, pending_order.id, item.id, original_qty + 2)
        
        assert item.quantity == original_qty + 2


class TestOrderBatch:
    """Test batch order operations"""
    
    def test_export_orders(self, db_session):
        """Test exporting orders"""
        from app.services.order_service import export_orders
        
        export_data = export_orders(db_session)
        
        assert export_data is not None
        assert len(export_data) > 0
