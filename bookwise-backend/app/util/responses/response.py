from flask import jsonify
from typing import Any, Optional

def create_response(status_code: int, message: str, data: Optional[Any] = None) -> tuple:
    """
    Create a standardized API response
    
    Args:
        status_code: HTTP status code
        message: Response message
        data: Optional data to include in response
        
    Returns:
        tuple: (response, status_code) for Flask
    """
    response = {
        'success': status_code < 400,
        'status_code': status_code,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return jsonify(response), status_code

def success_response(message: str, data: Optional[Any] = None, status_code: int = 200) -> tuple:
    """Create a success response"""
    return create_response(status_code, message, data)

def error_response(message: str, status_code: int = 400, data: Optional[Any] = None) -> tuple:
    """Create an error response"""
    return create_response(status_code, message, data)

def validation_error_response(message: str = "Validation failed", errors: Optional[Any] = None) -> tuple:
    """Create a validation error response"""
    data = {'errors': errors} if errors else None
    return create_response(422, message, data)

def not_found_response(message: str = "Resource not found") -> tuple:
    """Create a 404 not found response"""
    return create_response(404, message)

def unauthorized_response(message: str = "Unauthorized access") -> tuple:
    """Create a 401 unauthorized response"""
    return create_response(401, message)

def forbidden_response(message: str = "Forbidden access") -> tuple:
    """Create a 403 forbidden response"""
    return create_response(403, message)

def internal_server_error_response(message: str = "Internal server error") -> tuple:
    """Create a 500 internal server error response"""
    return create_response(500, message)