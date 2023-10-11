from configuration.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    description = Column(String(150), nullable=False)
    rating = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    def __init__(self, user_id, book_id, description, rating):
        self.user_id = user_id
        self.book_id = book_id
        self.description = description
        self.rating = rating
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id='{self.user_id}'," \
               f"book_id='{self.book_id}', description='{self.description}', rating='{self.rating}'," \
               f"last_update='{self.last_update}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "description": self.description,
            "rating": self.rating,
            "last_update": str(data_time_conversion.dataTimeConversionToSaoPaulo())
        }