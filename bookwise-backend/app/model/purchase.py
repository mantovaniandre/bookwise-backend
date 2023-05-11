from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from configuration.database import Base
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    price = Column(String(6))
    date = Column(DateTime, nullable=True, onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    def __init__(self, price, user_id, book_id):
        self.price = price
        self.date = data_time_conversion.dataTimeConversionToSaoPaulo()
        self.user_id = user_id
        self.book_id = book_id

    def __repr__(self):
        return f"<User(id={self.id}, price='{self.price}', date='{self.date}'," \
               f"user_id='{self.user_id}', book_id='{self.book_id}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "date": str(data_time_conversion.dataTimeConversionToSaoPaulo()),
            "user_id": self.user_id,
            "book_id": self.book_id
        }
