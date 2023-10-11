from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_route = Blueprint("comment_route", __name__)


@comment_route.route('/createComment', methods=['POST'])
@jwt_required()
def create_comment():
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        result = comment_service.create_purchase(id_user_token, request_data)
    except Exception as e:
        return response_error