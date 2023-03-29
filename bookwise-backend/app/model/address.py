from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from configuration.database import Base
from util.datatime import data_time_conversion
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    number = Column(String(10), nullable=False)
    complement = Column(String(255), nullable=True)
    neighborhood = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(2), nullable=False)
    zipcode = Column(String(9), nullable=False)
    country = Column(String(20), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='address')

    def __init__(self, **kwargs):
        self.street = kwargs.get('street')
        self.number = kwargs.get('number')
        self.complement = kwargs.get('complement')
        self.neighborhood = kwargs.get('neighborhood')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.zipcode = kwargs.get('zipcode')
        self.country = kwargs.get('country')
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', number='{self.number}', city='{self.city}', " \
               f"state='{self.state}', zipcode='{self.zipcode}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "country": self.country,
            "last_update": data_time_conversion.dataTimeConversionToSaoPaulo()
        }
