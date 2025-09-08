from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.payment_service import PaymentService
from util.responses.response import create_response

payment_route = Blueprint('payment', __name__)

@payment_route.route('/api/payments/create-intent', methods=['POST'])
@jwt_required()
def create_payment_intent():
    """Create a payment intent"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'amount' not in data:
            return create_response(400, "Amount is required")
        
        amount = data['amount']
        currency = data.get('currency', 'usd')
        metadata = data.get('metadata', {})
        metadata['user_id'] = current_user
        
        result = PaymentService.create_payment_intent(
            amount=amount,
            currency=currency,
            metadata=metadata
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Payment intent created successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@payment_route.route('/api/payments/confirm', methods=['POST'])
@jwt_required()
def confirm_payment():
    """Confirm a payment intent"""
    try:
        data = request.get_json()
        
        if not data or 'payment_intent_id' not in data:
            return create_response(400, "Payment intent ID is required")
        
        payment_intent_id = data['payment_intent_id']
        payment_method_id = data.get('payment_method_id')
        
        result = PaymentService.confirm_payment(
            payment_intent_id=payment_intent_id,
            payment_method_id=payment_method_id
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Payment confirmed successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@payment_route.route('/api/payments/methods', methods=['GET'])
@jwt_required()
def get_payment_methods():
    """Get user's saved payment methods"""
    try:
        current_user = get_jwt_identity()
        
        # TODO: Implement get payment methods from database
        # For now, return empty list
        return create_response(200, "Payment methods retrieved successfully", {
            'payment_methods': []
        })
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@payment_route.route('/api/payments/methods', methods=['POST'])
@jwt_required()
def save_payment_method():
    """Save a payment method"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'payment_method_id' not in data:
            return create_response(400, "Payment method ID is required")
        
        payment_method_id = data['payment_method_id']
        set_as_default = data.get('set_as_default', False)
        
        result = PaymentService.save_payment_method(
            user_id=current_user,
            payment_method_id=payment_method_id,
            set_as_default=set_as_default
        )
        
        return create_response(201, "Payment method saved successfully", {
            'payment_method': result.to_dict()
        })
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@payment_route.route('/api/payments/methods/<int:payment_method_id>', methods=['DELETE'])
@jwt_required()
def delete_payment_method(payment_method_id):
    """Delete a payment method"""
    try:
        current_user = get_jwt_identity()
        
        # TODO: Implement delete payment method
        # For now, return success
        return create_response(200, "Payment method deleted successfully")
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@payment_route.route('/api/payments/webhook', methods=['POST'])
def payment_webhook():
    """Handle Stripe webhooks"""
    try:
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')
        
        result = PaymentService.handle_payment_webhook(payload, sig_header)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500