from datetime import datetime
from sqlalchemy.orm import relationship
from jupyterhub.orm import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey,DateTime

from service.database import db


class Purchase(db.Model):
    __tablename__ = 'purchases'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, ForeignKey('books.id'),  nullable=False)
    total = db.Column(db.Float, nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="purchases")
    books = db.relationship("Book", back_populates="purchases")

    def __init__(self, user, total, purchase_date=None):
        self.user_id = user.id
        self.total = total

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'total': self.total, 'purchase_date': self.purchase_date}
