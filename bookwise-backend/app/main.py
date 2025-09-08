from flask import Flask, request
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from controller.book import book_route
from controller.login import login_route
from controller.purchase import purchase_route
from controller.user import user_route
from controller.cart import cart_route
from controller.order import order_route
from controller.payment import payment_route
from demo_routes import demo_route
from migration.initial_data import create_tables, create_user_type, drop_tables, create_gender, insert_books
from model.user import User
from model.address import Address
from model.user_type import UserType
from model.gender import Gender
from model.book import Book
from model.purchase import Purchase
from model.comment import Comment
from model.cart import Cart, CartItem
from model.order import Order, OrderItem
from model.payment_method import PaymentMethod
from flask_cors import CORS
from configuration.secret_key import Config
# from util.field_mapping.book import books
import logging

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

# Secure CORS configuration
CORS(app, resources={
    r"/api/*": {"origins": Config.CORS_ORIGINS},
    r"/*": {"origins": Config.CORS_ORIGINS}
})

# Rate limiting configuration
def get_user_id():
    try:
        return get_jwt_identity() or get_remote_address()
    except:
        return get_remote_address()

limiter = Limiter(
    key_func=get_user_id,
    default_limits=["1000 per hour"],
    storage_uri="memory://"
)
limiter.init_app(app)

# Configure logging
if Config.ENVIRONMENT == 'production':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(user_route)
app.register_blueprint(login_route)
app.register_blueprint(book_route)
app.register_blueprint(purchase_route)
app.register_blueprint(cart_route)
app.register_blueprint(order_route)
app.register_blueprint(payment_route)
app.register_blueprint(demo_route)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "BookWise API is running!"}, 200

if __name__ == "__main__":
    # Skip database operations for demo
    print("Starting BookWise E-commerce API...")
    print("Enhanced with:")
    print("   -> Shopping Cart System")
    print("   -> Order Management")
    print("   -> Stripe Payment Integration")
    print("   -> Secure JWT Authentication")
    print("   -> Rate Limiting & Security")
    print("   -> Commercial-Ready Features")
    print("\nAPI available at: http://localhost:5000")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
