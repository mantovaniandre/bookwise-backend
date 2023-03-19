from datetime import datetime
from service.database import db


class Address(db.Model):
    __tablename__ = 'addresses'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(10), nullable=False)
    complement = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', back_populates="addresses")

    def __init__(self, street, number, city, state, zipcode, country, complement=None, last_update=None):
        self.street = street
        self.number = number
        self.complement = complement
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.country = country

    def to_dict(self):
        return {'id': self.id, 'street': self.street, 'number': self.number, 'complement': self.complement,
                'city': self.city, 'state': self.state, 'zipcode': self.zipcode, 'country': self.country,
                'last_update': self.last_update}
