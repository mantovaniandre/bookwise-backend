from sqlalchemy import Column, Integer, String, Float, DateTime, func
from configuration.database import Base
from util.datatime.data_time_conversion import DataTimeConversion

data_time_conversion = DataTimeConversion()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    year = Column(String(10))
    isbn = Column(String(30))
    edition = Column(String(30))
    origin = Column(String(30))
    book_format = Column(String(30))
    binding = Column(String(30))
    language = Column(String(30))
    country = Column(String(50))
    pages = Column(String(4))
    stock = Column(String(4))
    url_img = Column(String(255))
    description = Column(String(255))
    price = Column(String(8))
    category = Column(String(20))
    last_update = Column(DateTime, nullable=True, onupdate=func.now())

    def __init__(self, title, author, year, isbn, edition, origin, book_format, binding, language,
                 country, pages, stock, url_img, description, price, category):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.edition = edition
        self.origin = origin
        self.book_format = book_format
        self.binding = binding
        self.language = language
        self.country = country
        self.pages = pages
        self.stock = stock
        self.url_img = url_img
        self.description = description
        self.price = price
        self.category = category
        self.last_update = data_time_conversion.dataTimeConversionToSaoPaulo()

    def __repr__(self):
        return f"<Book(id={self.id}, author='{self.author}'," \
               f"year='{self.year}', isbn='{self.isbn}', edition='{self.edition}', origin='{self.origin}'," \
               f"format='{self.format}', binding='{self.binding}', language='{self.language}'," \
               f"country='{self.country}', pages='{self.pages}', stock='{self.stock}', url_img='{self.url_img}', " \
               f"description='{self.description}', price='{self.price}',last_update='{self.last_update}'" \
               f"category='{self.category}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn,
            "edition": self.edition,
            "origin": self.origin,
            "book_format": self.book_format,
            "binding": self.binding,
            "language": self.language,
            "country": self.country,
            "pages": self.pages,
            "stock": self.stock,
            "url_img": self.url_img,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "last_update": str(data_time_conversion.dataTimeConversionToSaoPaulo())
        }
