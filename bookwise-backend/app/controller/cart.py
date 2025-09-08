from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.cart_service import CartService
from util.responses.response import create_response

cart_route = Blueprint('cart', __name__)

@cart_route.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart contents"""
    try:
        current_user = get_jwt_identity()
        result = CartService.get_cart_contents(current_user)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Cart retrieved successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@cart_route.route('/api/cart/items', methods=['POST'])
@jwt_required()
def add_cart_item():
    """Add item to cart"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'book_id' not in data:
            return create_response(400, "Book ID is required")
        
        book_id = data['book_id']
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            return create_response(400, "Quantity must be greater than 0")
        
        result = CartService.add_item_to_cart(current_user, book_id, quantity)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(201, "Item added to cart successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@cart_route.route('/api/cart/items/<int:cart_item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(cart_item_id):
    """Update cart item quantity"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return create_response(400, "Quantity is required")
        
        quantity = data['quantity']
        
        if quantity <= 0:
            return create_response(400, "Quantity must be greater than 0")
        
        result = CartService.update_cart_item(current_user, cart_item_id, quantity)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Cart item updated successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@cart_route.route('/api/cart/items/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(cart_item_id):
    """Remove item from cart"""
    try:
        current_user = get_jwt_identity()
        result = CartService.remove_cart_item(current_user, cart_item_id)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Item removed from cart successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@cart_route.route('/api/cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        current_user = get_jwt_identity()
        result = CartService.clear_cart(current_user)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        return create_response(200, "Cart cleared successfully", result)
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")

@cart_route.route('/api/cart/count', methods=['GET'])
@jwt_required()
def get_cart_count():
    """Get cart item count"""
    try:
        current_user = get_jwt_identity()
        result = CartService.get_cart_contents(current_user)
        
        if 'error' in result:
            return create_response(400, result['error'])
        
        cart_data = result.get('cart', {})
        count = cart_data.get('total_items', 0)
        
        return create_response(200, "Cart count retrieved successfully", {'count': count})
        
    except Exception as e:
        return create_response(500, f"Internal server error: {str(e)}")