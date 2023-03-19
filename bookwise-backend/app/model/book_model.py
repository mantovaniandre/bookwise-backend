from datetime import datetime
from sqlalchemy import ForeignKey
from service.database import db


class Book(db.Model):
    __tablename__ = 'books'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.utcnow)
    language = db.Column(db.String(50), nullable=False)
    isbn = db.Column(db.String(50), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    cart_items = db.relationship('CartItem', back_populates="books")
    purchases = db.relationship('Purchase', back_populates="books")
    ratings = db.relationship('Rating', back_populates="books")

    def __init__(self, title, author, publisher, publication_date, language, isbn, pages, price, description, stock):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_date = publication_date
        self.language = language
        self.isbn = isbn
        self.pages = pages
        self.price = price
        self.description = description
        self.stock = stock

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publication_date': self.publication_date,
            'language': self.language,
            'isbn': self.isbn,
            'pages': self.pages,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'last_update': self.last_update
        }
