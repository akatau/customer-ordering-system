from sqlalchemy.orm import Session

from ..models.cart import Cart, CartItem
from ..models.product import Product
from ..models.user import User


class CartService:
    @staticmethod
    def get_or_create_cart(db: Session, user: User) -> Cart:
        cart = db.query(Cart).filter(Cart.user_id == user.id).first()
        if cart is None:
            cart = Cart(user_id=user.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def get_cart(db: Session, user: User) -> Cart:
        return CartService.get_or_create_cart(db, user)

    @staticmethod
    def add_item(db: Session, user: User, product_id: str, quantity: int) -> Cart:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise ValueError("Product not found")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        cart = CartService.get_or_create_cart(db, user)
        item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.add(item)

        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def update_item(db: Session, user: User, product_id: str, quantity: int) -> Cart:
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

        cart = CartService.get_or_create_cart(db, user)
        item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        if item is None:
            raise ValueError("Cart item not found")

        item.quantity = quantity
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def remove_item(db: Session, user: User, product_id: str) -> Cart:
        cart = CartService.get_or_create_cart(db, user)
        item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        if item is None:
            raise ValueError("Cart item not found")
        db.delete(item)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def clear_cart(db: Session, user: User) -> Cart:
        cart = CartService.get_or_create_cart(db, user)
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
        db.refresh(cart)
        return cart
