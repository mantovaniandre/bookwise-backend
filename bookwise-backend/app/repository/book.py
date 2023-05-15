from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.book import Book
from util.datatime.data_time_conversion import DataTimeConversion
from util.exception.custom_exception import DatabaseError, BookNotFoundIdError, BookDeletionError, \
    NewBookCreationError, GetBookByLanguageError, GetBookByAuthorError

data_time_conversion = DataTimeConversion()


class BookRepository:
    @staticmethod
    def get_all_books():
        try:
            with Session() as session:
                query = session.query(Book)
                books = [book.to_dict() for book in query]
                return books
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

    @staticmethod
    def get_book_by_id(book_id):
        try:
            with Session() as session:
                book = session.query(Book).filter_by(id=book_id).first()
                if not book:
                    raise BookNotFoundIdError(book_id)
                return book
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    @staticmethod
    def update_book(book_id, **update_values):
        try:
            with Session() as session:
                book = session.query(Book).filter_by(id=book_id).first()
                if book:
                    for column, value in update_values.items():
                        setattr(book, column, value)
                    session.commit()
                    return True
                else:
                    raise Exception(f"Livro com ID {book_id} não encontrado.")
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    @staticmethod
    def verify_book_by_isbn(isbn):
        try:
            with Session() as session:
                book = session.query(Book).filter_by(isbn=isbn).first()
                return book
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    @staticmethod
    def verify_book_by_id(id):
        try:
            with Session() as session:
                book = session.query(Book).filter_by(id=id).first()
                return book
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))

    @staticmethod
    def create_book_to_database(new_book):
        with Session() as session:
            try:
                session.add(new_book)
                session.flush()
                session.refresh(new_book)
                book_id = new_book.id
                if book_id is not None:
                    session.commit()
                    return True
                else:
                    raise NewBookCreationError()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def delete_book_by_id(request_book_id):
        try:
            with Session() as session:
                book = session.query(Book).filter_by(id=request_book_id).first()
                if book is not None:
                    session.delete(book)
                    session.commit()
                    return True
                else:
                    raise BookDeletionError(request_book_id)
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

    @staticmethod
    def get_book_by_language(term):
        try:
            with Session() as session:
                books = session.query(Book).filter(Book.language.like(f'%{term}%')).all()
                books_dict = [book.to_dict() for book in books]
                if not books_dict:
                    raise GetBookByLanguageError(term)
                else:
                    return books_dict
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

    @staticmethod
    def get_book_by_title(term):
        try:
            with Session() as session:
                books = session.query(Book).filter(Book.title.like(f'%{term}%')).all()
                books_dict = [book.to_dict() for book in books]
                if not books_dict:
                    raise GetBookByLanguageError(term)
                else:
                    return books_dict
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

    @staticmethod
    def get_book_by_author(term):
        try:
            with Session() as session:
                books = session.query(Book).filter(Book.author.like(f'%{term}%')).all()
                books_dict = [book.to_dict() for book in books]
                if not books_dict:
                    raise GetBookByAuthorError(term)
                else:
                    return books_dict
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

