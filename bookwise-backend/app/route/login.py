from controller.login import LoginController
from flask import request, Blueprint
from util.response.login import LoginResponse


login_route = Blueprint("login_route", __name__)
# created instances
login_controller = LoginController()
login_response = LoginResponse()


@login_route.route('/login', methods=['POST'])
def login():
    try:
        user_data = request.get_json()
        token = login_controller.login(user_data)
        response_successful = login_response.response_login_successful(token)
        return response_successful
    except Exception as e:
        exception_error = str(e)
        response_error = login_response.response_error_login(exception_error)
        return response_error


