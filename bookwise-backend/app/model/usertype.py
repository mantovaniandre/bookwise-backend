from configuration.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class UserType(Base):
    __tablename__ = 'usertypes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='usertype')

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



