from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketCategory(str, Enum):
    ORDER_ISSUE = "order_issue"
    PRODUCT_QUESTION = "product_question"
    REFUND = "refund"
    SHIPPING = "shipping"
    RETURN = "return"
    OTHER = "other"


class TicketCreate(BaseModel):
    """Create a new support ticket."""
    subject: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10, max_length=5000)
    category: TicketCategory
    priority: Optional[TicketPriority] = TicketPriority.MEDIUM
    order_id: Optional[str] = None


class TicketUpdate(BaseModel):
    """Update support ticket status and priority."""
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_to: Optional[str] = None


class TicketAddNote(BaseModel):
    """Add internal note to support ticket."""
    note: str = Field(..., min_length=1, max_length=2000)


class TicketEscalate(BaseModel):
    """Escalate ticket to admin."""
    reason: str = Field(..., min_length=1, max_length=500)


class TicketBase(BaseModel):
    """Base ticket response."""
    id: str
    subject: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    order_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]


class TicketResponse(TicketBase):
    """Full ticket response."""
    user_id: str
    assigned_to: Optional[str]
    internal_notes: Optional[str]

    class Config:
        from_attributes = True


class TicketList(BaseModel):
    """List of tickets with pagination."""
    items: List[TicketResponse]
    total: int
    page: int
    limit: int
    pages: int


class OrderModification(BaseModel):
    """Modify order items or shipping details."""
    action: str = Field(..., pattern="^(add_item|remove_item|change_address)$")
    product_id: Optional[str] = None  # For add/remove item actions
    quantity: Optional[int] = None  # For add item action
    shipping_address: Optional[dict] = None  # For change_address action
    reason: str = Field(..., min_length=5, max_length=500)


class RefundRequest(BaseModel):
    """Process a refund for an order."""
    order_id: str
    reason: str = Field(..., min_length=10, max_length=500)
    amount: Optional[float] = None  # If None, refund full amount


class RefundResponse(BaseModel):
    """Refund processing response."""
    refund_id: str
    order_id: str
    amount: float
    status: str
    processed_at: datetime
    transaction_id: Optional[str]


class OrderModificationResponse(BaseModel):
    """Response from an order modification action."""
    order_id: str
    modifications: dict
    status: str
    audit_note: str


class ReportExportResponse(BaseModel):
    """Exported report response."""
    format: str
    content: str


class SalesReport(BaseModel):
    """Sales analytics report."""
    total_revenue: float
    total_orders: int
    average_order_value: float
    top_products: List[dict]
    sales_by_category: dict
    daily_breakdown: List[dict]
    period_start: datetime
    period_end: datetime


class InventoryReport(BaseModel):
    """Inventory status report."""
    total_products: int
    in_stock: int
    out_of_stock: int
    low_stock_alerts: List[dict]
    stock_by_category: dict
    total_value: float


class CustomerAnalytics(BaseModel):
    """Customer analytics report."""
    total_customers: int
    new_customers: int
    repeat_customers: int
    avg_lifetime_value: float
    conversion_rate: float
    cart_abandonment_rate: float
    top_customers: List[dict]


class ReportExportRequest(BaseModel):
    """Request report export."""
    format: str = Field(..., pattern="^(csv|json|pdf)$")
    report_type: str = Field(..., pattern="^(sales|inventory|customers)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
