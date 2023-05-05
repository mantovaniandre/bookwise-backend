from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from configuration.database import Session
from model.book import Book
from util.datatime.data_time_conversion import DataTimeConversion
from util.exception.custom_exception import BooksNotFoundError, DatabaseError, BookNotFoundIdError, BookDeletionError, \
    NewBookCreationError

session = Session()
data_time_conversion = DataTimeConversion()


class BookRepository:
    @staticmethod
    def get_book():
        try:
            book_instances = session.query(Book).distinct().all()
            books = [book_instance.to_dict() for book_instance in book_instances]
            if books is None:
                raise BooksNotFoundError()
            return books
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def get_book_by_id(book_id):
        try:
            book = session.query(Book).filter_by(id=book_id).first()
            if not book:
                raise BookNotFoundIdError(book_id)
            return book
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def update_book(book_id, **update_values):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE books SET last_update = '{now}', "
        for column, value in update_values.items():
            query += f"{column} = '{value}', "
        query = query[:-2]
        query += f" WHERE id = {book_id};"
        query = text(query)
        try:
            session.execute(query)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def verify_book_by_isbn(isbn):
        book = session.query(Book).filter_by(isbn=isbn).first()
        return book

    @staticmethod
    def verify_book_by_id(id):
        book = session.query(Book).filter_by(id=id).first()
        return book

    @staticmethod
    def save_book_to_database(new_book):
        try:
            session.add(new_book)
            session.commit()
            session.refresh(new_book)
            user_id = new_book.id
            if user_id is not None:
                return True
            else:
                session.rollback()
                raise NewBookCreationError()
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def delete_book_by_id(request_book_id):
        try:
            with Session() as session:
                address = session.query(Book).filter_by(id=request_book_id).first()
                if address is not None:
                    session.delete(address)
                    session.commit()
                    return True
                else:
                    raise BookDeletionError(request_book_id)
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))

