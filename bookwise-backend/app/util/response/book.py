from flask import Response
import json


@staticmethod
class BookResponse():
    @staticmethod
    def response_get_book_successfully(book):
        data = {"message": "book sent successfully",
                "status": "201",
                "content_type": "application/json",
                "book": book}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_get_book_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_updated_book_successfully():
        data = {"message": "book updated successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_updating_book_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_create_book_successfully():
        data = {"message": "book created successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_create_book_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_delete_book_successfully(book):
        data = {"message": f"book {book} delete successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_delete_book_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_search_book_successfully(books):
        data = {"message": f"book found successfully",
                "status": "201",
                "content_type": "application/json",
                "book": books}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_search_book_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

