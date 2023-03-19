from flask import Flask
from configuration.database_configuration import DatabaseConfiguration
from route.user_route import user_blueprint
from model.address_model import Address
from model.book_model import Book
from model.cartitem_model import CartItem
from model.creditcard_model import CreditCard
from model.purchase_model import Purchase
from model.rating_model import Rating
from model.user_model import User
from model.usertype_model import UserType
from service.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(DatabaseConfiguration)

    db.init_app(app)

    app.register_blueprint(user_blueprint)

    return app


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
