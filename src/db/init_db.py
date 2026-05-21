from sqlalchemy.orm import Session

from src.models import MenuItem

DEFAULT_MENU_ITEMS = [
    {"name": "Margherita", "size": "small", "base_price": 8.99},
    {"name": "Margherita", "size": "medium", "base_price": 11.99},
    {"name": "Margherita", "size": "large", "base_price": 14.99},
    {"name": "Pepperoni", "size": "small", "base_price": 9.99},
    {"name": "Pepperoni", "size": "medium", "base_price": 12.99},
    {"name": "Pepperoni", "size": "large", "base_price": 15.99},
]


def seed_menu_items(db: Session) -> None:
    if db.query(MenuItem).count() > 0:
        return

    db.add_all(MenuItem(**item) for item in DEFAULT_MENU_ITEMS)
    db.commit()
