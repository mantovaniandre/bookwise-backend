from flask import Flask
from flask_jwt_extended import JWTManager
from controller.book import book_route
from controller.login import login_route
from controller.purchase import purchase_route
from controller.user import user_route
from migration.initial_data import create_tables, create_user_type, drop_tables, create_gender, insert_books
from model.user import User
from model.address import Address
from model.user_type import UserType
from model.gender import Gender
from model.credit_card import CreditCard
from model.book import Book
from model.purchase import Purchase
from model.comment import Comment
from flask_cors import CORS
from configuration.secret_key import Config
from util.field_mapping.book import books

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(user_route)
app.register_blueprint(login_route)
app.register_blueprint(book_route)
app.register_blueprint(purchase_route)

if __name__ == "__main__":
    drop_tables()
    create_tables()
    create_user_type()
    create_gender()
    insert_books(books)
    app.run()
