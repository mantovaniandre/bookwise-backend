from flask import Response
import json


class UserReponse:
    @staticmethod
    def response_user_created_successfully():
        data = {"message": "user created successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_error_creating_user(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response
