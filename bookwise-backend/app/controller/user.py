from service.user import UserService


class UserController:
    @staticmethod
    def create_user(user_data):
        try:
            UserService.create_user(user_data)
        except Exception as e:
            raise ValueError(f"{e}")

    @staticmethod
    def update_user(front_data, id_token):
        try:
            UserService.update_user(front_data, id_token)
        except Exception as e:
            raise ValueError(f"{e}")
