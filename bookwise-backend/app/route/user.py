from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from configuration.database import Session
from controller.user import UserController
from util.response.user import UserReponse

user_route = Blueprint("user_route", __name__)
# created instances
user_controller = UserController()
user_response = UserReponse()
session = Session()


@user_route.route("/userCreate", methods=["POST"])
def create_user():
    try:
        user_data = request.get_json()
        user_controller.create_user(user_data)
        response_successful = user_response.response_user_created_successfully()
        return response_successful
    except Exception as e:
        exception_error = str(e)
        response_error = user_response.response_error_creating_user(exception_error)
        return response_error


@user_route.route('/userUpdate', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        front_data = request.get_json()
        get_id_token = get_jwt_identity()
        user_controller.update_user(front_data, get_id_token)
        response_successful = user_response.response_user_updated_successfully()
        return response_successful
    except Exception as e:
        exception_error = str(e)
        response_error = user_response.response_error_updating_user(exception_error)
        return response_error
