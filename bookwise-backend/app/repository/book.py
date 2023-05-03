from sqlalchemy.exc import SQLAlchemyError

from configuration.database import Session
from model.book import Book
from util.datatime.data_time_conversion import DataTimeConversion
from util.exception.custom_exception import BooksNotFoundError, DatabaseError, BookNotFoundIdError

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
