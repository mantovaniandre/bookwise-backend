from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from configuration.database import Base
from sqlalchemy.sql import func
import uuid
from enum import Enum as PyEnum

class OrderStatus(PyEnum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed' 
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'

class PaymentStatus(PyEnum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    order_number = Column(String(36), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Order details
    status = Column(String(20), default=OrderStatus.PENDING.value)
    payment_status = Column(String(20), default=PaymentStatus.PENDING.value)
    
    # Amounts
    subtotal = Column(Numeric(10, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(10, 2), default=0)
    shipping_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    
    # Payment information
    stripe_payment_intent_id = Column(String(100), nullable=True)
    payment_method_id = Column(Integer, ForeignKey('payment_methods.id'), nullable=True)
    
    # Shipping information
    shipping_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    shipped_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    payment_method = relationship('PaymentMethod')
    shipping_address = relationship('Address')

    def __init__(self, user_id, subtotal, total_amount, tax_amount=0, 
                 shipping_amount=0, discount_amount=0):
        self.user_id = user_id
        self.order_number = str(uuid.uuid4())
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.shipping_amount = shipping_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount

    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', " \
               f"user_id={self.user_id}, status='{self.status}', total={self.total_amount})>"

    def calculate_total(self):
        """Recalculate total amount based on components"""
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount
        return self.total_amount

    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PENDING.value, OrderStatus.CONFIRMED.value]

    def to_dict(self):
        return {
            "id": self.id,
            "order_number": self.order_number,
            "user_id": self.user_id,
            "status": self.status,
            "payment_status": self.payment_status,
            "subtotal": float(self.subtotal),
            "tax_amount": float(self.tax_amount),
            "shipping_amount": float(self.shipping_amount),
            "discount_amount": float(self.discount_amount),
            "total_amount": float(self.total_amount),
            "items": [item.to_dict() for item in self.items],
            "tracking_number": self.tracking_number,
            "notes": self.notes,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "shipped_at": str(self.shipped_at) if self.shipped_at else None,
            "delivered_at": str(self.delivered_at) if self.delivered_at else None
        }


class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    
    # Product details at time of purchase
    book_title = Column(String(200), nullable=False)  # Snapshot of book title
    book_author = Column(String(200), nullable=False)  # Snapshot of author
    unit_price = Column(Numeric(10, 2), nullable=False)  # Price at time of purchase
    quantity = Column(Integer, nullable=False, default=1)
    
    created_at = Column(DateTime, default=func.now())

    # Relationships
    order = relationship('Order', back_populates='items')
    book = relationship('Book')

    def __init__(self, order_id, book_id, book_title, book_author, unit_price, quantity):
        self.order_id = order_id
        self.book_id = book_id
        self.book_title = book_title
        self.book_author = book_author
        self.unit_price = unit_price
        self.quantity = quantity

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, book_title='{self.book_title}', " \
               f"quantity={self.quantity}, unit_price={self.unit_price})>"

    def get_subtotal(self):
        """Calculate subtotal for this order item"""
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "book_id": self.book_id,
            "book_title": self.book_title,
            "book_author": self.book_author,
            "unit_price": float(self.unit_price),
            "quantity": self.quantity,
            "subtotal": float(self.get_subtotal()),
            "created_at": str(self.created_at)
        }