from flask import request, Blueprint
from service.login import LoginService
from util.response.login import LoginResponse


login_route = Blueprint("login_route", __name__)
# created instances

login_response = LoginResponse()
login_service = LoginService()


@login_route.route('/login', methods=['POST'])
def login():
    try:
        request_data = request.get_json()
        token = login_service.login(request_data)
        response_successful = login_response.response_login_successful(token)
        return response_successful
    except Exception as e:
        response_error = login_response.response_error_login(str(e))
        return response_error



