from flask import Blueprint, request
from controller.book import BookController
from util.response.book import BookResponse

book_route = Blueprint("book_route", __name__)
book_controller = BookController()
book_response = BookResponse()


@book_route.route('/getBooks', methods=['GET'])
def get_books():
    try:
        book = book_controller.get_book()
        response_successful = book_response.response_get_book_successfully(book)
        return response_successful
    except Exception as e:
        response_error = book_response.response_error_get_book(str(e))
        return response_error


@book_route.route('/getBookById/<book_id>', methods=['GET'])
def get_books_by_id(book_id):
    try:
        book = book_controller.get_book_by_id(book_id)
        response_successful = book_response.response_get_book_successfully(book)
        return response_successful
    except Exception as e:
        response_error = book_response.response_error_get_book(str(e))
        return response_error

