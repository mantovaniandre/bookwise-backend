from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from configuration.database import Base
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    price = Column(String(6))
    quantity = Column(String(4))
    date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    def __init__(self, price, quantity, user_id, book_id):
        self.price = price
        self. quantity = quantity
        self.date = data_time_conversion.dataTimeConversionToSaoPaulo()
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"<User(id={self.id}, price='{self.price}', quantity='{self.quantity}', date='{self.date}'," \
               f"user_id='{self.user_id}', book_id='{self.book_id}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "quantity": self.quantity,
            "date": str(self.date),
            "user_id": self.user_id,
            "book_id": self.book_id
        }
