from flask import Flask
from configuration.database import Base, engine
from model.user import User
from model.address import Address
from model.usertype import UserType
from route.user import user_route

app = Flask(__name__)

app.register_blueprint(user_route, url_prefix="/user")


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
