from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Product, Order, AdminLog
from ..schemas.admin import (
    AdminLogListResponse,
    AdminLogResponse,
    ProductCreateRequest,
    ProductUpdateRequest,
    UserAdminListResponse,
    UserAdminResponse,
    UserUpdateAdminRequest,
    OrderAdminListResponse,
    OrderAdminResponse,
    OrderUpdateAdminRequest,
    BulkImportResponse,
    ExportResponse,
)
from ..services.admin_service import AdminService
from .deps import require_admin, require_admin_only

router = APIRouter(prefix="/admin", tags=["admin"])


# Product Management
@router.post("/products", response_model=dict)
def create_product(
    product_data: ProductCreateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Create a new product (Admin only)."""
    admin_service = AdminService(db)
    product = admin_service.create_product(product_data, current_admin.id)
    return {"product_id": product.id, "message": "Product created successfully"}


@router.put("/products/{product_id}", response_model=dict)
def update_product(
    product_id: str,
    update_data: ProductUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Update an existing product (Admin only)."""
    admin_service = AdminService(db)
    product = admin_service.update_product(product_id, update_data, current_admin.id)
    return {"product_id": product.id, "message": "Product updated successfully"}


@router.delete("/products/{product_id}", status_code=204)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Delete a product (Admin only)."""
    admin_service = AdminService(db)
    admin_service.delete_product(product_id, current_admin.id)


@router.post("/products/bulk-import", response_model=BulkImportResponse)
def bulk_import_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Import products from CSV file (Admin only)."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")

    content = file.file.read().decode('utf-8')
    admin_service = AdminService(db)
    return admin_service.bulk_import_products(content, current_admin.id)


@router.get("/products/export", response_model=ExportResponse)
def export_products_csv(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Export all products to CSV (Admin/Support)."""
    admin_service = AdminService(db)
    csv_content = admin_service.export_products_csv()
    # In a real implementation, upload to storage and return URL
    # For now, return as data URL
    import base64
    encoded = base64.b64encode(csv_content.encode()).decode()
    export_url = f"data:text/csv;base64,{encoded}"

    admin_service.log_admin_action(
        admin_user_id=current_admin.id,
        action="export_products",
        resource_type="system",
    )

    return ExportResponse(
        export_url=export_url,
        message="Products exported successfully"
    )


# User Management
@router.get("/users", response_model=UserAdminListResponse)
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Get paginated list of users (Admin only)."""
    admin_service = AdminService(db)
    users = admin_service.get_users(skip, limit)
    return UserAdminListResponse(users=users)


@router.put("/users/{user_id}", response_model=UserAdminResponse)
def update_user(
    user_id: str,
    update_data: UserUpdateAdminRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Update a user (Admin only)."""
    admin_service = AdminService(db)
    user = admin_service.update_user(user_id, update_data, current_admin.id)
    return user


@router.delete("/users/{user_id}", status_code=204)
def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Deactivate a user (Admin only)."""
    admin_service = AdminService(db)
    admin_service.deactivate_user(user_id, current_admin.id)


# Order Management
@router.get("/orders", response_model=OrderAdminListResponse)
def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Get paginated list of all orders (Admin/Support)."""
    admin_service = AdminService(db)
    orders = admin_service.get_orders(skip, limit)
    return OrderAdminListResponse(orders=orders)


@router.put("/orders/{order_id}", response_model=OrderAdminResponse)
def update_order(
    order_id: str,
    update_data: OrderUpdateAdminRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Update an order (Admin/Support)."""
    admin_service = AdminService(db)
    order = admin_service.update_order(order_id, update_data, current_admin.id)
    return order


@router.get("/orders/{order_id}/invoice", response_model=dict)
def generate_invoice(
    order_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    """Generate invoice for an order (Admin/Support)."""
    admin_service = AdminService(db)
    invoice_url = admin_service.generate_invoice(order_id, current_admin.id)
    return {"invoice_url": invoice_url, "message": "Invoice generated successfully"}


# Activity Logs
@router.get("/activity-logs", response_model=AdminLogListResponse)
def get_activity_logs(
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin_only),
):
    """Get filtered activity logs (Admin only)."""
    admin_service = AdminService(db)
    logs = admin_service.get_activity_logs(
        user_id=user_id,
        action=action,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return AdminLogListResponse(logs=logs)
