from configuration.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DateTimeHelper


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    
    # User preferences and status
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    
    # Foreign keys
    primary_address_id = Column(Integer, ForeignKey('addresses.id'), nullable=True)
    user_type_id = Column(Integer, ForeignKey('user_types.id'), default=2)  # Default to CLIENT
    gender_id = Column(Integer, ForeignKey('genders.id'), nullable=True)
    
    # JWT and session management
    token = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)

    # Relationships  
    primary_address = relationship('Address', foreign_keys=[primary_address_id], post_update=True)
    address = relationship('Address', back_populates='user', uselist=False)
    user_type = relationship('UserType', back_populates='users', lazy='joined')
    gender = relationship('Gender', back_populates='users', lazy='joined')
    
    # New relationships for e-commerce
    payment_methods = relationship('PaymentMethod', back_populates='user', cascade='all, delete-orphan')
    cart = relationship('Cart', back_populates='user', uselist=False, cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, phone=None, 
                 date_of_birth=None, primary_address_id=None, user_type_id=2, gender_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.primary_address_id = primary_address_id
        self.user_type_id = user_type_id
        self.gender_id = gender_id

    def __repr__(self):
        return f"<User(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}', " \
               f"email='{self.email}', is_active={self.is_active})>"

    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @property 
    def is_admin(self):
        """Check if user is admin"""
        return self.user_type and self.user_type.type_name == 'ADMIN'

    def get_active_cart(self):
        """Get user's active cart or create new one"""
        if not self.cart or self.cart.status != 'active':
            from model.cart import Cart
            self.cart = Cart(user_id=self.id)
        return self.cart

    def to_dict(self, include_sensitive=False):
        """
        Convert user to dictionary
        
        Args:
            include_sensitive: Whether to include sensitive data like password hash
        """
        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "is_active": self.is_active,
            "email_verified": self.email_verified,
            "user_type": self.user_type.to_dict() if self.user_type else None,
            "gender": self.gender.to_dict() if self.gender else None,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "last_login": str(self.last_login) if self.last_login else None
        }
        
        if include_sensitive:
            user_dict["password"] = self.password
            user_dict["token"] = self.token
            
        return user_dict


