from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from configuration.database import Base
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class CreditCard(Base):
    __tablename__ = 'credit_cards'

    id = Column(Integer, primary_key=True)
    cardNumber = Column(String(20), nullable=False)
    typeCard = Column(String(20), nullable=False)
    flag = Column(String(20), nullable=True)
    bank = Column(String(20), nullable=False)
    countryBank = Column(String(20), nullable=False)
    cardName = Column(String(20), nullable=False)
    expiration = Column(String(10), nullable=False)
    cvv = Column(String(5), nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='credit_card')
    user_versions = relationship('UserVersion', back_populates='credit_card')

    def __init__(self, cardNumber, typeCard, flag, bank, countryBank, cardName, expiration, cvv):
        self.cardNumber = cardNumber
        self.typeCard = typeCard
        self.flag = flag
        self.bank = bank
        self.countryBank = countryBank
        self.cardName = cardName
        self.expiration = expiration
        self.cvv = cvv
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<CreditCard(id={self.id}, cardNumber='{self.cardNumber}', typeCard='{self.typeCard}', " \
               f"flag='{self.flag}', bank='{self.bank}', countryBank='{self.countryBank}'," \
               f"cardName='{self.cardName}', expiration='{self.expiration}', cvv='{self.cvv}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "cardNumber": self.cardNumber,
            "typeCard": self.typeCard,
            "flag": self.flag,
            "bank": self.bank,
            "countryBank": self.countryBank,
            "cardName": self.cardName,
            "expiration": self.expiration,
            "cvv": self.cvv,
            "last_update": data_time_conversion.dataTimeConversionToSaoPaulo()
        }
