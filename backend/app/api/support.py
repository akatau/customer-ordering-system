"""Support ticket API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User, UserRole
from ..models.ticket import Ticket, TicketStatus
from ..api.deps import get_current_user, require_role
from ..services.support_service import (
    SupportService,
    RefundService,
    OrderModificationService,
)
from ..schemas.support import (
    TicketCreate,
    TicketUpdate,
    TicketAddNote,
    TicketEscalate,
    TicketResponse,
    TicketList,
    OrderModification,
    RefundRequest,
    RefundResponse,
)

router = APIRouter(tags=["support"])


@router.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new support ticket."""
    ticket = SupportService.create_ticket(db, current_user.id, ticket_data)
    return TicketResponse.from_orm(ticket)


@router.get("/tickets", response_model=TicketList)
def list_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: TicketStatus = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List support tickets.
    
    Regular users see only their own tickets.
    Support/admin see all tickets.
    """
    # Filter by current user if not support/admin
    user_id_filter = None
    if current_user.role == UserRole.customer:
        user_id_filter = current_user.id

    tickets, total = SupportService.list_tickets(
        db,
        skip=skip,
        limit=limit,
        status=status,
        user_id=user_id_filter,
    )

    return TicketList(
        items=[TicketResponse.from_orm(t) for t in tickets],
        total=total,
        page=skip // limit + 1,
        limit=limit,
        pages=(total + limit - 1) // limit,
    )


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get ticket details."""
    ticket = SupportService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Check authorization
    if current_user.role == UserRole.customer and ticket.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")

    return TicketResponse.from_orm(ticket)


@router.put("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: str,
    update_data: TicketUpdate,
    current_user: User = Depends(require_role([UserRole.support, UserRole.admin])),
    db: Session = Depends(get_db),
):
    """Update ticket status and assignment.
    
    Only support/admin users can update tickets.
    """
    ticket = SupportService.update_ticket(db, ticket_id, update_data)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketResponse.from_orm(ticket)


@router.post("/tickets/{ticket_id}/notes", response_model=TicketResponse)
def add_note(
    ticket_id: str,
    note_data: TicketAddNote,
    current_user: User = Depends(require_role([UserRole.support, UserRole.admin])),
    db: Session = Depends(get_db),
):
    """Add internal note to ticket."""
    ticket = SupportService.add_note(db, ticket_id, note_data.note)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketResponse.from_orm(ticket)


@router.post("/tickets/{ticket_id}/escalate", response_model=TicketResponse)
def escalate_ticket(
    ticket_id: str,
    current_user: User = Depends(require_role([UserRole.support, UserRole.admin])),
    db: Session = Depends(get_db),
):
    """Escalate ticket to admin."""
    ticket = SupportService.escalate_ticket(db, ticket_id, current_user.id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketResponse.from_orm(ticket)
