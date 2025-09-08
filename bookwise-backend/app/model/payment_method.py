from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from configuration.database import Base
from sqlalchemy.sql import func

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Stripe payment method details (tokenized)
    stripe_payment_method_id = Column(String(100), nullable=False)  # pm_xxxxxxxx
    payment_type = Column(String(20), nullable=False)  # card, bank_account, etc.
    
    # Card details (last 4 digits and brand for display)
    last_four = Column(String(4), nullable=True)  # Only last 4 digits for display
    brand = Column(String(20), nullable=True)     # visa, mastercard, amex, etc.
    exp_month = Column(Integer, nullable=True)
    exp_year = Column(Integer, nullable=True)
    
    # Metadata
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='payment_methods')

    def __init__(self, user_id, stripe_payment_method_id, payment_type, 
                 last_four=None, brand=None, exp_month=None, exp_year=None, is_default=False):
        self.user_id = user_id
        self.stripe_payment_method_id = stripe_payment_method_id
        self.payment_type = payment_type
        self.last_four = last_four
        self.brand = brand
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.is_default = is_default

    def __repr__(self):
        return f"<PaymentMethod(id={self.id}, user_id={self.user_id}, type='{self.payment_type}', " \
               f"brand='{self.brand}', last_four='****{self.last_four}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "payment_type": self.payment_type,
            "brand": self.brand,
            "last_four": self.last_four,
            "exp_month": self.exp_month,
            "exp_year": self.exp_year,
            "is_default": self.is_default,
            "is_active": self.is_active,
            "created_at": str(self.created_at)
        }