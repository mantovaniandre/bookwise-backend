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
    street = Column(String(100), nullable=False)
    number = Column(String(6), nullable=False)
    complement = Column(String(50), nullable=True)
    neighborhood = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(9), nullable=False)
    country = Column(String(6), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='address', lazy='joined')

    def __init__(self, street, number, complement, neighborhood, city, state, zip_code, country):
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.street}', number='{self.number}', city='{self.city}', " \
               f"state='{self.state}', zip_code='{self.zip_code}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "neighborhood": self.neighborhood,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "last_update": str(data_time_conversion.dataTimeConversionToSaoPaulo())
        }
