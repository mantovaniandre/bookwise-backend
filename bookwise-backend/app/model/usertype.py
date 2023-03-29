from configuration.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


class UserType(Base):
    __tablename__ = 'usertypes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.last_update = datetime.utcnow()

    def __repr__(self):
        return f"<UserType(id={self.description})>"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "last_update": self.last_update.isoformat()
        }




