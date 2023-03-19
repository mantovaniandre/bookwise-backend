from datetime import datetime
from sqlalchemy import ForeignKey
from service.database import db


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, ForeignKey('books.id'))
    quantity = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="cart_items")
    books = db.relationship('Book', back_populates="cart_items")

    def __init__(self, product_id, quantity):
        self.product_id = product_id
        self.quantity = quantity

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'product_id': self.product_id,
                'quantity': self.quantity, 'last_update': self.last_update}
