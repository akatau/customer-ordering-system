"""Support service for handling tickets, refunds, and order modifications."""
import uuid
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session

from ..models.ticket import Ticket, TicketStatus, TicketPriority, TicketCategory
from ..models.order import Order, OrderStatus
from ..models.user import User
from ..schemas.support import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    OrderModification,
    RefundRequest,
    RefundResponse,
)


class SupportService:
    """Handle all support-related operations."""

    @staticmethod
    def create_ticket(
        db: Session, 
        user_id: str, 
        ticket_data: TicketCreate
    ) -> Ticket:
        """Create a new support ticket."""
        ticket = Ticket(
            id=str(uuid.uuid4()),
            user_id=user_id,
            subject=ticket_data.subject,
            description=ticket_data.description,
            category=ticket_data.category,
            priority=ticket_data.priority,
            order_id=ticket_data.order_id,
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def get_ticket(db: Session, ticket_id: str) -> Optional[Ticket]:
        """Retrieve ticket by ID."""
        return db.query(Ticket).filter(Ticket.id == ticket_id).first()

    @staticmethod
    def list_tickets(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        status: Optional[TicketStatus] = None,
        user_id: Optional[str] = None,
    ) -> tuple[List[Ticket], int]:
        """List tickets with optional filtering."""
        query = db.query(Ticket)
        
        if status:
            query = query.filter(Ticket.status == status)
        if user_id:
            query = query.filter(Ticket.user_id == user_id)
        
        total = query.count()
        tickets = query.offset(skip).limit(limit).all()
        
        return tickets, total

    @staticmethod
    def update_ticket(
        db: Session,
        ticket_id: str,
        update_data: TicketUpdate,
    ) -> Optional[Ticket]:
        """Update ticket status, priority, or assignment."""
        ticket = SupportService.get_ticket(db, ticket_id)
        if not ticket:
            return None

        if update_data.status:
            ticket.status = update_data.status
            if update_data.status == TicketStatus.RESOLVED:
                ticket.resolved_at = datetime.utcnow()

        if update_data.priority:
            ticket.priority = update_data.priority

        if update_data.assigned_to:
            ticket.assigned_to = update_data.assigned_to

        ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def add_note(db: Session, ticket_id: str, note: str) -> Optional[Ticket]:
        """Add an internal note to a ticket."""
        ticket = SupportService.get_ticket(db, ticket_id)
        if not ticket:
            return None

        current_notes = ticket.internal_notes or ""
        timestamp = datetime.utcnow().isoformat()
        new_note = f"[{timestamp}] {note}\n"
        ticket.internal_notes = current_notes + new_note
        ticket.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(ticket)
        return ticket

    @staticmethod
    def escalate_ticket(db: Session, ticket_id: str, admin_id: str) -> Optional[Ticket]:
        """Escalate ticket to admin."""
        ticket = SupportService.get_ticket(db, ticket_id)
        if not ticket:
            return None

        ticket.assigned_to = admin_id
        ticket.priority = TicketPriority.HIGH
        ticket.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(ticket)
        return ticket


class RefundService:
    """Handle refund processing."""

    @staticmethod
    def process_refund(
        db: Session,
        order_id: str,
        reason: str,
        amount: Optional[float] = None,
    ) -> dict:
        """Process refund for an order.
        
        Returns dict with refund_id, status, and transaction details.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"Order {order_id} not found")

        if order.status == OrderStatus.cancelled:
            raise ValueError("Cannot refund cancelled order")

        refund_amount = amount or float(order.total_amount)
        
        # Stub payment provider integration
        # In production, this would call Stripe/PayPal refund API
        refund_id = f"refund_{uuid.uuid4().hex[:12]}"
        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"

        # Update order status
        order.status = OrderStatus.cancelled
        order.updated_at = datetime.utcnow()
        db.commit()

        return {
            "refund_id": refund_id,
            "order_id": order_id,
            "amount": refund_amount,
            "status": "completed",
            "processed_at": datetime.utcnow().isoformat(),
            "transaction_id": transaction_id,
        }


class OrderModificationService:
    """Handle order modifications by support team."""

    @staticmethod
    def modify_order(
        db: Session,
        order_id: str,
        modification: OrderModification,
        support_user_id: str,
    ) -> dict:
        """Modify an existing order.
        
        Supports: adding items, removing items, changing address.
        """
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError(f"Order {order_id} not found")

        if order.status != OrderStatus.pending:
            raise ValueError(f"Cannot modify order with status {order.status}")

        modifications = {
            "action": modification.action,
            "reason": modification.reason,
            "modified_by": support_user_id,
            "modified_at": datetime.utcnow().isoformat(),
        }

        if modification.action == "change_address":
            if modification.shipping_address:
                order.shipping_address = str(modification.shipping_address)
                modifications["new_address"] = modification.shipping_address

        elif modification.action in ["add_item", "remove_item"]:
            # These would require additional logic to manipulate OrderItems
            # Stub for now
            modifications["product_id"] = modification.product_id
            modifications["quantity"] = modification.quantity

        order.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(order)

        # Create audit log
        audit_note = f"Order modified: {modification.action} - {modification.reason}"
        
        return {
            "order_id": order_id,
            "modifications": modifications,
            "status": "success",
            "audit_note": audit_note,
        }
