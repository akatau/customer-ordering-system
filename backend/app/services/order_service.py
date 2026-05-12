from decimal import Decimal
from sqlalchemy.orm import Session

from ..models.cart import CartItem
from ..models.order import Order, OrderItem, OrderStatus
from ..models.product import Product
from ..services.payment_service import PaymentService


class OrderService:
    @staticmethod
    def create_order(db: Session, user_id: str, shipping_address: str, billing_address: str | None, payment_method: str, items_data: list[dict]) -> Order:
        products = {product.id: product for product in db.query(Product).filter(Product.id.in_([item["product_id"] for item in items_data])).all()}
        if len(products) != len(items_data):
            raise ValueError("One or more products are not available")

        total_amount = Decimal("0.00")
        order_items = []

        for item in items_data:
            product = products[item["product_id"]]
            if item["quantity"] < 1:
                raise ValueError("Quantity must be at least 1")
            if product.stock_quantity < item["quantity"]:
                raise ValueError(f"Insufficient stock for product {product.name}")

            line_total = Decimal(product.price) * item["quantity"]
            total_amount += line_total
            order_items.append(
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item["quantity"],
                    unit_price=product.price,
                    total_price=line_total,
                )
            )

        payment_result = PaymentService.process_payment(total_amount, payment_method)
        if payment_result["status"] != "succeeded":
            raise ValueError("Payment failed")

        order = Order(
            user_id=user_id,
            shipping_address=shipping_address,
            billing_address=billing_address,
            status=OrderStatus.processing,
            total_amount=total_amount,
            items=order_items,
        )
        db.add(order)

        for item in order_items:
            product = products[item.product_id]
            product.stock_quantity -= item.quantity

        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def list_orders(db: Session, user_id: str) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).all()

    @staticmethod
    def get_order(db: Session, user_id: str, order_id: str) -> Order | None:
        return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
