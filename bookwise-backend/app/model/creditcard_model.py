from datetime import datetime
from sqlalchemy import ForeignKey

from service.database import db


class CreditCard(db.Model):
    __tablename__ = 'credit_cards'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    card_number = db.Column(db.String(19), nullable=False)
    card_holder = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.String(20), nullable=False)
    cvv = db.Column(db.String(4), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="creditcards")

    def __init__(self, card_number, card_holder, expiration_date, cvv):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.cvv = cvv

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'card_number': self.card_number,
                'card_holder': self.card_holder, 'expiration_date': self.expiration_date, 'cvv': self.cvv,
                'last_update': self.last_update}
