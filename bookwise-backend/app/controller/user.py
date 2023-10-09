from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.user import UserService
from util.response.user import UserResponse

user_route = Blueprint("user_route", __name__)
# created instances
user_service = UserService()
user_response = UserResponse()


@user_route.route("/createUser", methods=["POST"])
def create_user():
    try:
        request_data = request.get_json()
        user_service.create_user(request_data)
        response_successful = user_response.response_user_created_successfully()
        return response_successful
    except Exception as e:
        response_error = user_response.response_error_creating_user(str(e))
        return response_error


@user_route.route('/updateUser', methods=['PUT'])
@jwt_required()
def update_user():
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        user_service.update_user(request_data, id_user_token)
        response_successful = user_response.response_user_updated_successfully()
        return response_successful
    except Exception as e:
        response_error = user_response.response_error_updating_user(str(e))
        return response_error


@user_route.route('/deleteUser', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        id_user_token = get_jwt_identity()
        user_service.delete_user(id_user_token)
        response_successful = user_response.response_user_deleted_successfully()
        return response_successful
    except Exception as e:
        response_error = user_response.response_error_deleted_user(str(e))
        return response_error


@user_route.route('/profileUser', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        id_token = get_jwt_identity()
        user = user_service.get_profile_user(id_token)
        response_successful = user_response.response_get_user_profile_successfully(user)
        return response_successful
    except Exception as e:
        response_error = user_response.response_error_updating_user(str(e))
        return response_error
