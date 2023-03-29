from service.user import UserService


class UserController:
    @staticmethod
    def create_user(user_data):
        UserService.save_user(user_data)

