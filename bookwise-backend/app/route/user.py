from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from configuration.database import Session
from controller.user import UserController
from util.exception.custom_exception import UserCreationError, UserUpdateError
from util.response.user import UserResponse

user_route = Blueprint("user_route", __name__)
# created instances
user_controller = UserController()
user_response = UserResponse()
session = Session()


@user_route.route("/userCreate", methods=["POST"])
def create_user():
    try:
        request_data = request.get_json()
        user_controller.create_user(request_data)
        response_successful = user_response.response_user_created_successfully()
        return response_successful
    except Exception as e:
        session.rollback()
        response_error = user_response.response_error_creating_user(str(e))
        return response_error
    finally:
        session.close()


@user_route.route('/userUpdate', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        request_data = request.get_json()
        id_token = get_jwt_identity()
        user_controller.update_user(request_data, id_token)
        response_successful = user_response.response_user_updated_successfully()
        return response_successful
    except Exception as e:
        session.rollback()
        response_error = user_response.response_error_updating_user(str(e))
        return response_error
    finally:
        session.close()


@user_route.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        id_token = get_jwt_identity()
        user = user_controller.get_profile_user(id_token)
        response_successful = user_response.response_get_user_profile_successfully(user)
        return response_successful
    except Exception as e:
        session.rollback()
        response_error = user_response.response_error_updating_user(str(e))
        return response_error
    finally:
        session.close()
