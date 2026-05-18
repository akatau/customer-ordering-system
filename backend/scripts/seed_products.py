from decimal import Decimal
import sys
from pathlib import Path

# Ensure project root is on sys.path so we can import app package
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import os

# Force SQLite DB for local seeding when running script directly
os.environ.setdefault("DATABASE_URL", f"sqlite:///./customer_ordering.db")

from app.database import SessionLocal, engine
from app.models.product import Product
from app.models.base import Base


def seed():
    # ensure tables exist (useful when running script directly)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        samples = [
            {
                "name": "Classic Coffee Mug",
                "description": "Ceramic mug with ergonomic handle.",
                "category": "home",
                "image_url": "http://127.0.0.1:3000/images/mug-v2.svg",
                "price": Decimal("12.99"),
                "stock_quantity": 120,
            },
            {
                "name": "Wireless Headphones",
                "description": "Over-ear noise-cancelling headphones.",
                "category": "electronics",
                "image_url": "http://127.0.0.1:3000/images/headphones-v2.svg",
                "price": Decimal("89.99"),
                "stock_quantity": 45,
            },
            {
                "name": "Running Shoes",
                "description": "Lightweight running shoes for daily training.",
                "category": "sports",
                "image_url": "http://127.0.0.1:3000/images/shoes-v2.svg",
                "price": Decimal("59.99"),
                "stock_quantity": 80,
            },
            {
                "name": "Bluetooth Speaker",
                "description": "Portable speaker with deep bass.",
                "category": "electronics",
                "image_url": "http://127.0.0.1:3000/images/speaker-v2.svg",
                "price": Decimal("39.99"),
                "stock_quantity": 200,
            },
            {
                "name": "Notebook - Lined",
                "description": "Hardcover lined notebook, 200 pages.",
                "category": "stationery",
                "image_url": "http://127.0.0.1:3000/images/notebook-v2.svg",
                "price": Decimal("7.49"),
                "stock_quantity": 300,
            },
        ]

        existing_products = {
            product.name: product
            for product in db.query(Product).all()
        }

        for p in samples:
            product = existing_products.get(p["name"])
            if product is None:
                product = Product(
                    name=p["name"],
                    description=p["description"],
                    category=p["category"],
                    image_url=p["image_url"],
                    price=p["price"],
                    stock_quantity=p["stock_quantity"],
                )
                db.add(product)
            else:
                product.description = p["description"]
                product.category = p["category"]
                product.image_url = p["image_url"]
                product.price = p["price"]
                product.stock_quantity = p["stock_quantity"]
        db.commit()
        print(f"Seeded or updated {len(samples)} products")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
