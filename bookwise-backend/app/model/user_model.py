from datetime import datetime
from sqlalchemy import ForeignKey
from service.database import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, ForeignKey('addresses.id'), nullable=False)
    user_type_id = db.Column(db.Integer, ForeignKey('user_types.id'), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    addresses = db.relationship("Address", back_populates="users")
    cart_items = db.relationship("CartItem", back_populates="users")
    creditcards = db.relationship("CreditCard", back_populates="users")
    ratings = db.relationship("Rating", back_populates="users")
    purchases = db.relationship("Purchase", back_populates="users")
    user_types = db.relationship("UserType", back_populates="users")

    def __init__(self, first_name, last_name, phone, cpf, email, password, address, user_type, gender, birthday, last_update=None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.cpf = cpf
        self.email = email
        self.password = password
        self.address_id = address.id
        self.user_type_id = user_type.id
        self.gender = gender
        self.birthday = birthday
        self.last_update = last_update or datetime.datetime.utcnow()

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'phone': self.phone,
                'cpf': self.cpf, 'email': self.email, 'password': self.password, 'address_id': self.address_id,
                'user_type_id': self.user_type_id, 'gender': self.gender, 'birthday': self.birthday,
                'last_update': self.last_update}