from configuration.database import Session
from service.book import BookService

book_service = BookService()
session = Session()


class BookController:
    @staticmethod
    def get_book():
        try:
            book = book_service.get_book()
            return book
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def get_book_by_id(book_id):
        try:
            book = book_service.get_book_by_id(book_id)
            return book
        except Exception as e:
            session.rollback()
            raise e