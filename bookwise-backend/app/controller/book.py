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

    @staticmethod
    def update_book(request_data, id_user_token, request_book_id):
        try:
            book_service.update_book(request_data, id_user_token, request_book_id)
            return True
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    def create_book(request_data, id_user_token):
        try:
            book_service.create_book(request_data, id_user_token)
            return True
        except Exception as e:
            session.rollback()
            raise e
