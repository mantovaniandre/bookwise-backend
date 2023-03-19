from datetime import datetime
from sqlalchemy.orm import relationship
from jupyterhub.orm import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime

from service.database import db


class Rating(db.Model):
    __tablename__ = 'ratings'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, ForeignKey('books.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)

    users = db.relationship("User", back_populates="ratings")
    books = db.relationship("Book", back_populates="ratings")

    def __init__(self, product_id, score):
        self.product_id = product_id
        self.score = score

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'product_id': self.product_id, 'score': self.score,
                'last_update': self.last_update}
