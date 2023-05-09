from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.book import Book
from util.datatime.data_time_conversion import DataTimeConversion
from util.exception.custom_exception import BooksNotFoundError, DatabaseError, BookNotFoundIdError, BookDeletionError, \
    NewBookCreationError


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
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE books SET last_update = '{now}', "

        for column, value in update_values.items():
            query += f"{column} = :{column}, "

        query = query[:-2]
        query += f" WHERE id = :book_id;"

        try:
            with Session() as session:
                session.query(Book).filter_by(id=book_id).update(update_values)
                session.commit()
            return True
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
    def save_book_to_database(new_book):
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




