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
    def response_error_get_book(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_book_updated_successfully():
        data = {"message": "book updated successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_error_updating_book(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

