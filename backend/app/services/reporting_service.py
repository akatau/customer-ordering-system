from datetime import datetime
from typing import Any, Dict, List, Optional
import json
from sqlalchemy import func, case
from sqlalchemy.orm import Session

from ..models import Product, Order, OrderItem, Cart, CartItem, User


class ReportingService:
    """Generate analytic reports from the database."""

    @staticmethod
    def sales_report(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        query = db.query(Order).filter(Order.status == "completed")
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)

        total_revenue = float(query.with_entities(func.coalesce(func.sum(Order.total_amount), 0)).scalar() or 0)
        total_orders = query.count()
        average_order_value = float(total_revenue / total_orders) if total_orders else 0.0

        top_products_query = (
            db.query(
                OrderItem.product_id,
                OrderItem.product_name,
                func.sum(OrderItem.quantity).label("quantity_sold"),
                func.sum(OrderItem.total_price).label("total_revenue"),
            )
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.status == "completed")
        )
        if start_date:
            top_products_query = top_products_query.filter(Order.created_at >= start_date)
        if end_date:
            top_products_query = top_products_query.filter(Order.created_at <= end_date)

        top_products = [
            {
                "product_id": row.product_id,
                "product_name": row.product_name,
                "quantity_sold": int(row.quantity_sold),
                "total_revenue": float(row.total_revenue),
            }
            for row in top_products_query.group_by(OrderItem.product_id, OrderItem.product_name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(10)
        ]

        category_query = (
            db.query(
                Product.category,
                func.coalesce(func.sum(OrderItem.total_price), 0).label("category_revenue"),
            )
            .join(OrderItem, Product.id == OrderItem.product_id)
            .join(Order, OrderItem.order_id == Order.id)
            .filter(Order.status == "completed")
        )
        if start_date:
            category_query = category_query.filter(Order.created_at >= start_date)
        if end_date:
            category_query = category_query.filter(Order.created_at <= end_date)

        sales_by_category = {
            row.category: float(row.category_revenue)
            for row in category_query.group_by(Product.category).all()
        }

        dates_query = (
            db.query(
                func.date(Order.created_at).label("order_date"),
                func.count(Order.id).label("order_count"),
                func.coalesce(func.sum(Order.total_amount), 0).label("revenue"),
            )
            .filter(Order.status == "completed")
        )
        if start_date:
            dates_query = dates_query.filter(Order.created_at >= start_date)
        if end_date:
            dates_query = dates_query.filter(Order.created_at <= end_date)

        daily_breakdown = [
            {
                "date": row.order_date,
                "orders": int(row.order_count),
                "revenue": float(row.revenue),
            }
            for row in dates_query.group_by("order_date").order_by("order_date").all()
        ]

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "average_order_value": average_order_value,
            "top_products": top_products,
            "sales_by_category": sales_by_category,
            "daily_breakdown": daily_breakdown,
            "period_start": start_date or datetime.utcnow(),
            "period_end": end_date or datetime.utcnow(),
        }

    @staticmethod
    def inventory_report(db: Session) -> Dict[str, Any]:
        total_products = db.query(func.count(Product.id)).scalar() or 0
        in_stock = db.query(func.count(Product.id)).filter(Product.stock_quantity > 0).scalar() or 0
        out_of_stock = db.query(func.count(Product.id)).filter(Product.stock_quantity == 0).scalar() or 0
        low_stock_items = [
            {
                "product_id": product.id,
                "name": product.name,
                "stock_quantity": product.stock_quantity,
            }
            for product in db.query(Product).filter(Product.stock_quantity < 10).all()
        ]
        stock_by_category = {
            row.category: int(row.product_count)
            for row in (
                db.query(
                    Product.category,
                    func.coalesce(func.sum(Product.stock_quantity), 0).label("product_count"),
                )
                .group_by(Product.category)
                .all()
            )
        }
        total_value = float(db.query(func.coalesce(func.sum(Product.price * Product.stock_quantity), 0)).scalar() or 0)

        # Include both legacy and new keys to support API schema and tests
        return {
            "total_products": int(total_products),
            "in_stock": int(in_stock),
            "out_of_stock": int(out_of_stock),
            "in_stock_count": int(in_stock),
            "out_of_stock_count": int(out_of_stock),
            "low_stock_alerts": low_stock_items,
            "low_stock_items": low_stock_items,
            "stock_by_category": stock_by_category,
            "total_value": total_value,
            "total_inventory_value": total_value,
        }

    @staticmethod
    def customer_analytics(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Dict[str, Any]:
        if start_date and end_date:
            customer_filter = db.query(User).filter(User.created_at >= start_date, User.created_at <= end_date)
        elif start_date:
            customer_filter = db.query(User).filter(User.created_at >= start_date)
        else:
            customer_filter = db.query(User)

        total_customers = customer_filter.count()
        new_customers = customer_filter.count()
        repeat_customers = (
            db.query(User.id)
            .join(Order, User.id == Order.user_id)
            .group_by(User.id)
            .having(func.count(Order.id) > 1)
            .count()
        )
        total_order_value = float(db.query(func.coalesce(func.sum(Order.total_amount), 0)).scalar() or 0)
        avg_lifetime_value = float(total_order_value / total_customers) if total_customers else 0.0
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        average_order_value = float(total_order_value / total_orders) if total_orders else 0.0
        conversion_rate = float(total_customers and (total_orders) / total_customers or 0.0)

        cart_count = db.query(func.count(Cart.id)).scalar() or 0
        abandoned_carts = db.query(func.count(Cart.id)).join(CartItem).scalar() or 0
        cart_abandonment_rate = float(abandoned_carts / cart_count) if cart_count else 0.0

        top_customers = [
            {
                "user_id": row.user_id,
                "total_spent": float(row.total_spent),
            }
            for row in (
                db.query(Order.user_id, func.coalesce(func.sum(Order.total_amount), 0).label("total_spent"))
                .group_by(Order.user_id)
                .order_by(func.sum(Order.total_amount).desc())
                .limit(10)
                .all()
            )
        ]

        return {
            "total_customers": int(total_customers),
            "new_customers": int(new_customers),
            "repeat_customers": int(repeat_customers),
            "avg_lifetime_value": avg_lifetime_value,
            "conversion_rate": conversion_rate,
            "cart_abandonment_rate": cart_abandonment_rate,
            "top_customers": top_customers,
            "total_orders": int(total_orders),
            "average_order_value": average_order_value,
        }

    @staticmethod
    def export_report(db: Session, report_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, export_format: str = "json") -> Dict[str, Any]:
        if report_type == "sales":
            report = ReportingService.sales_report(db, start_date, end_date)
        elif report_type == "inventory":
            report = ReportingService.inventory_report(db)
        elif report_type == "customers":
            report = ReportingService.customer_analytics(db, start_date, end_date)
        else:
            raise ValueError("Invalid report type")
        if export_format == "json":
            return {"format": "json", "content": json.dumps(report, default=str)}

        if export_format == "csv":
            return ReportingService._export_report_csv(report_type, report)

        raise ValueError("Unsupported export format")

    @staticmethod
    def _export_report_csv(report_type: str, report: Dict[str, Any]) -> Dict[str, Any]:
        rows = []
        if report_type == "sales":
            rows.append(["metric", "value"])
            for key in ["total_revenue", "total_orders", "average_order_value"]:
                rows.append([key, report[key]])
        elif report_type == "inventory":
            rows.append(["metric", "value"])
            rows.append(["total_products", report["total_products"]])
            rows.append(["in_stock", report["in_stock"]])
            rows.append(["out_of_stock", report["out_of_stock"]])
            rows.append(["total_value", report["total_value"]])
        elif report_type == "customers":
            rows.append(["metric", "value"])
            rows.append(["total_customers", report["total_customers"]])
            rows.append(["new_customers", report["new_customers"]])
            rows.append(["repeat_customers", report["repeat_customers"]])
            rows.append(["avg_lifetime_value", report["avg_lifetime_value"]])
        else:
            raise ValueError("Unsupported report type")

        csv_lines = [",".join(map(str, row)) for row in rows]
        return {"format": "csv", "content": "\n".join(csv_lines)}
