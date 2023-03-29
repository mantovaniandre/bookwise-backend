from model.usertype import UserType


class UsertypeService:
    @staticmethod
    def create_usertype(**kwargs):
        new_usertype = UserType(**kwargs)
        return new_usertype
