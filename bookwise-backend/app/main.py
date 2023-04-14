from flask import Flask
from migration.initial_data import create_tables, create_userType, drop_tables, create_gender
from model.user import User
from model.address import Address
from model.usertype import UserType
from model.gender import Gender
from model.creditCard import CreditCard
from route.login import login_route
from route.user import user_route
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(user_route)
app.register_blueprint(login_route)


if __name__ == "__main__":
    # drop_tables()
    create_tables()
    create_userType()
    create_gender()
    app.run(debug=True)
