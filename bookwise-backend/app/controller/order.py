from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.order_service import OrderService
from service.payment_service import PaymentService
from util.responses.response import create_response

order_route = Blueprint('order', __name__)

@order_route.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create order from cart"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json() or {}
        
        payment_method_id = data.get('payment_method_id')
        shipping_address_id = data.get('shipping_address_id')
        
        # Create order from cart
        result = OrderService.create_order_from_cart(
            user_id=current_user,
            payment_method_id=payment_method_id,
            shipping_address_id=shipping_address_id
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        order = result['order']
        
        # Create payment intent for the order
        payment_result = PaymentService.process_order_payment(order['id'])
        
        if 'error' in payment_result:
            return create_response(400, f"Payment processing error: {payment_result['error']}")
        
        return create_response(201, "Order created successfully", {
            'order': order,
            'payment': payment_result
        })
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@order_route.route('/api/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get user's orders"""
    try:
        current_user = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)  # Max 50 per page
        status = request.args.get('status')
        
        result = OrderService.get_user_orders(
            user_id=current_user,
            status=status,
            page=page,
            per_page=per_page
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Orders retrieved successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@order_route.route('/api/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order_details(order_id):
    """Get order details"""
    try:
        current_user = get_jwt_identity()
        result = OrderService.get_order_details(order_id, current_user)
        
        if 'error' in result:
            return create_response(404, result['error'])
        
        return create_response(200, "Order details retrieved successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@order_route.route('/api/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        current_user = get_jwt_identity()
        result = OrderService.cancel_order(order_id, current_user)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Order cancelled successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

# Admin routes
@order_route.route('/api/admin/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    """Get all orders (admin only)"""
    try:
        # TODO: Add admin role check
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        
        # For now, return user orders (would need admin check)
        current_user = get_jwt_identity()
        result = OrderService.get_user_orders(
            user_id=current_user,
            status=status,
            page=page,
            per_page=per_page
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "All orders retrieved successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@order_route.route('/api/admin/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status (admin only)"""
    try:
        # TODO: Add admin role check
        data = request.get_json()
        
        if not data or 'status' not in data:
            return create_response(400, "Status is required")
        
        status = data['status']
        tracking_number = data.get('tracking_number')
        
        result = OrderService.update_order_status(
            order_id=order_id,
            status=status,
            tracking_number=tracking_number
        )
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Order status updated successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")