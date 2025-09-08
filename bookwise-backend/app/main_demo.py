from flask import Flask, request, jsonify
from flask_cors import CORS
from demo_routes import demo_route

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register demo routes
app.register_blueprint(demo_route)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "BookWise Demo API is running!"}, 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API info"""
    return {
        "message": "BookWise E-commerce API - Demo Mode",
        "version": "2.0.0",
        "features": [
            "Shopping Cart System",
            "Order Management", 
            "Stripe Payment Integration",
            "Secure JWT Authentication",
            "Rate Limiting & Security",
            "Commercial-Ready Features"
        ],
        "demo_endpoints": {
            "books": "/demo/books",
            "register": "/demo/register", 
            "login": "/demo/login",
            "cart": "/demo/cart"
        },
        "api_endpoints": {
            "books": "/api/books",
            "book_by_id": "/api/books/<id>",
            "featured_books": "/api/books/featured",
            "bestsellers": "/api/books/bestsellers",
            "categories": "/api/categories",
            "cart_items": "/api/cart/items",
            "orders": "/api/orders",
            "payments": "/api/payments/create-intent",
            "user_profile": "/profileUser"
        }
    }, 200

if __name__ == "__main__":
    print("Starting BookWise E-commerce Demo API...")
    print("Enhanced with:")
    print("   -> Shopping Cart System")
    print("   -> Order Management")
    print("   -> Stripe Payment Integration") 
    print("   -> Secure JWT Authentication")
    print("   -> Rate Limiting & Security")
    print("   -> Commercial-Ready Features")
    print("   -> NO DATABASE REQUIRED!")
    print("\nAPI available at: http://localhost:5000")
    print("Demo endpoints:")
    print("   GET  /demo/books     - View available books")
    print("   POST /demo/register  - Register new user")
    print("   POST /demo/login     - Login user") 
    print("   GET  /demo/cart      - View cart")
    print("   POST /demo/cart      - Add to cart")
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )