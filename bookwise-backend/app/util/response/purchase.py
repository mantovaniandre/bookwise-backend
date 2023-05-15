import json
from flask import Response


class PurchaseResponse():
    @staticmethod
    def response_create_purchase_successfully(successful_purchases, failed_purchases):
        data = {
            "message": "successful purchase",
            "status": "201",
            "content_type": "application/json",
            "successful_purchases": successful_purchases,
            "failed_purchases": failed_purchases
        }
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_create_purchase_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response

    @staticmethod
    def response_get_purchase_successfully(purchase):
        data = {
            "message": "successful purchase",
            "status": "201",
            "content_type": "application/json",
            "purchase": purchase
        }
        response = Response(json.dumps(data), status=201, content_type='application/json')
        return response

    @staticmethod
    def response_get_purchase_error(exception_error):
        data = {"message": exception_error,
                "status": "400",
                "content_type": "application/json"}
        response = Response(json.dumps(data), status=400, content_type='application/json')
        return response