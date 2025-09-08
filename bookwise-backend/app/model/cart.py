from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from configuration.database import Base
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DateTimeHelper

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20), default='active')  # active, abandoned, converted
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='cart')
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, status='{self.status}')>"

    def get_total_amount(self):
        """Calculate total amount of all items in cart"""
        return sum(item.get_subtotal() for item in self.items)

    def get_total_items(self):
        """Get total quantity of items in cart"""
        return sum(item.quantity for item in self.items)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "total_amount": float(self.get_total_amount()),
            "total_items": self.get_total_items(),
            "items": [item.to_dict() for item in self.items],
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price at time of adding to cart
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    cart = relationship('Cart', back_populates='items')
    book = relationship('Book', lazy='joined')

    def __init__(self, cart_id, book_id, quantity, unit_price):
        self.cart_id = cart_id
        self.book_id = book_id
        self.quantity = quantity
        self.unit_price = unit_price

    def __repr__(self):
        return f"<CartItem(id={self.id}, cart_id={self.cart_id}, book_id={self.book_id}, " \
               f"quantity={self.quantity}, unit_price={self.unit_price})>"

    def get_subtotal(self):
        """Calculate subtotal for this cart item"""
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "book_id": self.book_id,
            "book": self.book.to_dict() if self.book else None,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "subtotal": float(self.get_subtotal()),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }