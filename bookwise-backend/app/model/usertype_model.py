from datetime import datetime
from service.database import db


class UserType(db.Model):
    __tablename__ = 'user_types'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(100), nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', back_populates="user_types")

    def __init__(self, type_name, last_update):
        self.type_name = type_name

    def to_dict(self):
        return {'id': self.id, 'type_name': self.type_name, 'last_update': self.last_update}
