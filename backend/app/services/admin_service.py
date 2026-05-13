import csv
import io
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import User, Product, Order, OrderItem, AdminLog
from ..schemas.admin import (
    ProductCreateRequest,
    ProductUpdateRequest,
    UserUpdateAdminRequest,
    OrderUpdateAdminRequest,
    BulkImportResponse,
)


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def log_admin_action(
        self,
        admin_user_id: str,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Log an admin action for audit purposes."""
        log_entry = AdminLog(
            admin_user_id=admin_user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        self.db.add(log_entry)
        self.db.commit()

    # Product Management
    def create_product(self, product_data: ProductCreateRequest, admin_user_id: str) -> Product:
        """Create a new product."""
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            stock_quantity=product_data.stock_quantity,
            image_url=product_data.image_url,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="create_product",
            resource_type="product",
            resource_id=product.id,
            details={"name": product.name, "category": product.category},
        )
        return product

    def update_product(
        self, product_id: str, update_data: ProductUpdateRequest, admin_user_id: str
    ) -> Product:
        """Update an existing product."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(product, key, value)

        product.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(product)

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="update_product",
            resource_type="product",
            resource_id=product.id,
            details=update_dict,
        )
        return product

    def delete_product(self, product_id: str, admin_user_id: str):
        """Delete a product."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if product is in any orders
        order_count = (
            self.db.query(Order)
            .join(OrderItem)
            .filter(OrderItem.product_id == product_id)
            .count()
        )
        if order_count > 0:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete product that has been ordered"
            )

        product_details = {"name": product.name, "category": product.category}
        self.db.delete(product)
        self.db.commit()

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="delete_product",
            resource_type="product",
            resource_id=product_id,
            details=product_details,
        )

    def bulk_import_products(self, csv_content: str, admin_user_id: str) -> BulkImportResponse:
        """Import products from CSV."""
        reader = csv.DictReader(io.StringIO(csv_content))
        imported_count = 0
        errors = []

        for row_num, row in enumerate(reader, start=2):  # Start at 2 for header
            try:
                product_data = ProductCreateRequest(
                    name=row["name"].strip(),
                    description=row["description"].strip(),
                    price=float(row["price"]),
                    category=row["category"].strip(),
                    stock_quantity=int(row["stock_quantity"]),
                    image_url=row.get("image_url", "").strip() or None,
                )
                self.create_product(product_data, admin_user_id)
                imported_count += 1
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")

        return BulkImportResponse(imported_count=imported_count, errors=errors)

    def export_products_csv(self) -> str:
        """Export all products to CSV."""
        products = self.db.query(Product).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "description", "price", "category", "stock_quantity", "image_url", "created_at"])

        for product in products:
            writer.writerow([
                product.id,
                product.name,
                product.description,
                product.price,
                product.category,
                product.stock_quantity,
                product.image_url or "",
                product.created_at.isoformat(),
            ])

        return output.getvalue()

    # User Management
    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get paginated list of users."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def update_user(self, user_id: str, update_data: UserUpdateAdminRequest, admin_user_id: str) -> User:
        """Update a user."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_dict = update_data.model_dump(exclude_unset=True)
        old_values = {}
        for key in update_dict:
            old_values[key] = getattr(user, key)

        for key, value in update_dict.items():
            setattr(user, key, value)

        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="update_user",
            resource_type="user",
            resource_id=user.id,
            details={"old_values": old_values, "new_values": update_dict},
        )
        return user

    def deactivate_user(self, user_id: str, admin_user_id: str):
        """Deactivate a user."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role == "admin":
            raise HTTPException(status_code=400, detail="Cannot deactivate admin user")

        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="deactivate_user",
            resource_type="user",
            resource_id=user.id,
            details={"email": user.email},
        )

    # Order Management
    def get_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get paginated list of all orders."""
        return self.db.query(Order).offset(skip).limit(limit).all()

    def update_order(self, order_id: str, update_data: OrderUpdateAdminRequest, admin_user_id: str) -> Order:
        """Update an order."""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        old_status = order.status
        order.status = update_data.status
        order.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(order)

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="update_order",
            resource_type="order",
            resource_id=order.id,
            details={"old_status": old_status, "new_status": update_data.status},
        )
        return order

    def generate_invoice(self, order_id: str, admin_user_id: str) -> str:
        """Generate invoice URL for an order."""
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # In a real implementation, this would generate a PDF and upload to storage
        # For now, return a mock URL
        invoice_url = f"/invoices/{order_id}.pdf"

        self.log_admin_action(
            admin_user_id=admin_user_id,
            action="generate_invoice",
            resource_type="order",
            resource_id=order.id,
        )

        return invoice_url

    # Activity Logs
    def get_activity_logs(
        self,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AdminLog]:
        """Get filtered activity logs."""
        query = self.db.query(AdminLog)

        if user_id:
            query = query.filter(AdminLog.admin_user_id == user_id)
        if action:
            query = query.filter(AdminLog.action == action)
        if start_date:
            query = query.filter(AdminLog.timestamp >= start_date)
        if end_date:
            query = query.filter(AdminLog.timestamp <= end_date)

        return query.order_by(AdminLog.timestamp.desc()).offset(skip).limit(limit).all()