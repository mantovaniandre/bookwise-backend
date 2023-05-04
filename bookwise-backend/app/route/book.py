from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.book import BookController, session
from util.response.book import BookResponse

book_route = Blueprint("book_route", __name__)
book_controller = BookController()
book_response = BookResponse()


@book_route.route('/getAllBooks', methods=['GET'])
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


@book_route.route('/updateBookById/<request_book_id>', methods=['PUT'])
@jwt_required()
def update_book(request_book_id):
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        book_controller.update_book(request_data, id_user_token, request_book_id)
        response_successful = book_response.response_book_updated_successfully()
        return response_successful
    except Exception as e:
        session.rollback()
        response_error = book_response.response_error_updating_book(str(e))
        return response_error
    finally:
        session.close()


@book_route.route('/createBook', methods=['PUT'])
@jwt_required()
def create_book():
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        book_controller.create_book(request_data, id_user_token)
        response_successful = book_response.response_create_book_successfully()
        return response_successful
    except Exception as e:
        session.rollback()
        response_error = book_response.response_error_create_book(str(e))
        return response_error
    finally:
        session.close()

