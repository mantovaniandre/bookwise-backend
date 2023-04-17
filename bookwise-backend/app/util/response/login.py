from flask import Response
import json


class LoginResponse:
        @staticmethod
        def response_login_successful(token):
            data = {"message": "successful login",
                    "token": token,
                    "status": "201",
                    "content_type": "application/json"}
            response = Response(json.dumps(data), status=201, content_type='application/json')
            return response

        @staticmethod
        def response_error_login(exception_error):
            data = {"message": exception_error,
                    "status": "400",
                    "content_type": "application/json"}
            response = Response(json.dumps(data), status=400, content_type='application/json')
            return response
