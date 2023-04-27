from model.userversion import UserVersion


class UserVersionService:
    @staticmethod
    def create_new_user_version(user_id, address_id, credit_card_id, data):
        new_user_version = UserVersion(
            user_id=user_id,
            address_id=address_id,
            credit_card_id=credit_card_id,
            data=data
        )
        if new_user_version:
            return new_user_version
        else:
            raise ValueError(f"error creating new user version.")
