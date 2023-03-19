from flask import Blueprint, request, jsonify
from controller.user_controller import UserController

user_blueprint = Blueprint('user', __name__ )


@user_blueprint.route('/user', methods=['POST'])
def create_user_route():
    data = request.get_json()
    user_controller = UserController
    result = user_controller.create_user(data)
    return result
