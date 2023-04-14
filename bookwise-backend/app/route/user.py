from flask import Blueprint, request
from configuration.database import Session
from controller.user import UserController
from util.response.user import UserReponse

user_route = Blueprint("user_route", __name__)
# created instances
user_controller = UserController()
user_response = UserReponse()
session = Session()


@user_route.route("/register", methods=["POST"])
def register_user():
    try:
        user_data = request.get_json()
        user_controller.register_user(user_data)
        response_successful = user_response.response_user_created_successfully()
        return response_successful
    except Exception as e:
        exception_error = str(e)
        response_error = user_response.response_error_creating_user(exception_error)
        return response_error
