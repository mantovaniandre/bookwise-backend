from flask import Response
import json


class UserResponse:
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

    @staticmethod
    def response_user_updated_successfully():
        data = {"message": "user updated successfully",
                "status": "201",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_get_user_profile_successfully(user):
        data = {"message": "profile sent successfully",
                "status": "201",
                "content_type": "application/json",
                "user": user}
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_error_updating_user(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response
