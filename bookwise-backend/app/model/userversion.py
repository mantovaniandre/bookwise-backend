from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from configuration.database import Base
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class UserVersion(Base):
    __tablename__ = 'user_version'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    address_id = Column(Integer, ForeignKey('addresses.id'))
    credit_card_id = Column(Integer, ForeignKey('credit_cards.id'))
    data = Column(String(500))
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='user_versions')
    address = relationship("Address", back_populates='user_versions')
    credit_card = relationship("CreditCard", back_populates='user_versions')

    def __init__(self, user_id, address_id, credit_card_id, data):
        self.user_id = user_id
        self.address_id = address_id
        self.credit_card_id = credit_card_id
        self.data = data
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<UserVersion(id={self.id}, user_id='{self.user_id}', address_id='{self.address_id}'," \
               f"credit_card_id='{self.credit_card_id}', data='{self.data}', last_update='{self.last_update}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "address_id": self.address_id,
            "credit_card_id": self.credit_card_id,
            "last_update": data_time_conversion.dataTimeConversionToSaoPaulo(),
        }