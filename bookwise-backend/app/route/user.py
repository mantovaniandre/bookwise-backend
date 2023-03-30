from flask import Blueprint, request, jsonify
from configuration.database import Session
from controller.user import UserController
from repository.user import UserRepository
from util.response.user import UserReponse

# created instances
user_route = Blueprint("user_route", __name__)
user_controller = UserController()
repository = UserRepository()
user_response = UserReponse()
session = Session()


@user_route.route("/register", methods=["POST"])
def register_user():
    try:
        user_data = request.get_json()
        user_controller.register_user(user_data)
        return user_response.response_user_created_successfully()
    except Exception as e:
        exception_error = str(e)
        return user_response.response_error_creating_user(exception_error)
