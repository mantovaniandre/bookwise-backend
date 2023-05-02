from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from configuration.database import Base
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class CreditCard(Base):
    __tablename__ = 'credit_cards'

    id = Column(Integer, primary_key=True)
    card_number = Column(String(20), nullable=False)
    type_card = Column(String(20), nullable=False)
    flag = Column(String(20), nullable=True)
    bank = Column(String(50), nullable=False)
    country_bank = Column(String(20), nullable=False)
    card_name = Column(String(30), nullable=False)
    expiration = Column(String(10), nullable=False)
    cvv = Column(String(10), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='credit_card', lazy='joined')

    def __init__(self, card_number, type_card, flag, bank, country_bank, card_name, expiration, cvv):
        self.card_number = card_number
        self.type_card = type_card
        self.flag = flag
        self.bank = bank
        self.country_bank = country_bank
        self.card_name = card_name
        self.expiration = expiration
        self.cvv = cvv
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<CreditCard(id={self.id}, card_number='{self.card_number}', type_card='{self.type_card}', " \
               f"flag='{self.flag}', bank='{self.bank}', country_bank='{self.country_bank}'," \
               f"card_name='{self.card_name}', expiration='{self.expiration}', cvv='{self.cvv}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "card_number": self.card_number,
            "type_card": self.type_card,
            "flag": self.flag,
            "bank": self.bank,
            "country_bank": self.country_bank,
            "card_name": self.card_name,
            "expiration": self.expiration,
            "cvv": self.cvv,
            "last_update": str(data_time_conversion.dataTimeConversionToSaoPaulo())
        }
