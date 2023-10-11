from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.purchase import PurchaseService
from util.response.purchase import PurchaseResponse

purchase_route = Blueprint("purchase_route", __name__)
purchase_response = PurchaseResponse()
purchase_service = PurchaseService()


@purchase_route.route('/createPurchase', methods=['POST'])
@jwt_required()
def create_purchase():
    try:
        request_data = request.get_json()
        id_user_token = get_jwt_identity()
        result = purchase_service.create_purchase(id_user_token, request_data)

        successful_purchases = result['successful_purchases']
        failed_purchases = result['failed_purchases']

        response_successful = purchase_response.response_create_purchase_successfully(successful_purchases,
                                                                                      failed_purchases)
        return response_successful
    except Exception as e:
        response_error = purchase_response.response_create_purchase_error(str(e))
        return response_error


@purchase_route.route('/getPurchase', methods=['GET'])
@jwt_required()
def get_purchase():
    try:
        id_user_token = get_jwt_identity()
        purchase = purchase_service.get_purchase(id_user_token)
        response_successful = purchase_response.response_get_purchase_successfully(purchase)
        return response_successful
    except Exception as e:
        response_error = purchase_response.response_get_purchase_error(str(e))
        return response_error
