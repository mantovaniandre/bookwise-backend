from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text

from configuration.database import Session
from service.book import BookService
from util.response.book import BookResponse

book_route = Blueprint("book_route", __name__)
book_response = BookResponse()
book_service = BookService()


@book_route.route('/getAllBooks', methods=['GET'])
def get_all_books():
    try:
        book = book_service.get_all_books()
        response_successful = book_response.response_get_book_successfully(book)
        return response_successful
    except Exception as e:
        response_error = book_response.response_get_book_error(str(e))
        return response_error


@book_route.route('/getBookById/<book_id>', methods=['GET'])
def get_book_by_id(book_id):
    try:
        book = book_service.get_book_by_id(book_id)
        response_successful = book_response.response_get_book_successfully(book)
        return response_successful
    except Exception as e:
        response_error = book_response.response_get_book_error(str(e))
        return response_error


@book_route.route('/updateBookById/<request_book_id>', methods=['PUT'])
@jwt_required()
def update_book(request_book_id):
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        book_service.update_book(request_data, id_user_token, request_book_id)
        response_successful = book_response.response_updated_book_successfully()
        return response_successful
    except Exception as e:
        response_error = book_response.response_updating_book_error(str(e))
        return response_error


@book_route.route('/createBook', methods=['PUT'])
@jwt_required()
def create_book():
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        book_service.create_book(request_data, id_user_token)
        response_successful = book_response.response_create_book_successfully()
        return response_successful
    except Exception as e:
        response_error = book_response.response_create_book_error(str(e))
        return response_error


@book_route.route('/deleteBookById/<request_book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(request_book_id):
    try:
        id_user_token = get_jwt_identity()
        book = book_service.delete_book(id_user_token, request_book_id)
        response_successful = book_response.response_delete_book_successfully(book['title'])
        return response_successful
    except Exception as e:
        response_error = book_response.response_delete_book_error(str(e))
        return response_error

