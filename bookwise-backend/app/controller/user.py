from service.user import UserService


class UserController:
    @staticmethod
    def register_user(user_data):
        UserService.register_user(user_data)

