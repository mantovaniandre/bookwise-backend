from configuration.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class UserType(Base):
    __tablename__ = 'user_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(10), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='user_type', lazy='joined')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<UserType(id={self.description})>"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "last_update": data_time_conversion.dataTimeConversionToSaoPaulo()
        }



