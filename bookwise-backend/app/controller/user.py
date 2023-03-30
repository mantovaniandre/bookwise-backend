from service.user import UserService


class UserController:
    @staticmethod
    def register_user(user_data):
        try:
            UserService.register_user(user_data)
        except Exception as e:
            raise ValueError(f"{e}")

