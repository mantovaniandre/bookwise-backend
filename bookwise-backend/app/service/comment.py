from service.book import user_repository
from service.purchase import PurchaseService

purchase_service = PurchaseService()


class CommentService:
    @staticmethod
    def create_comment(id_user_token, request_data):
        user = user_repository.get_user_by_id(id_user_token)
        if not user:
            raise Exception('Authentication failed. Invalid or expired token.')

        if user.user_type_id == 1:
            raise Exception('Admin user cannot make comment.')

        purchase_service.get_purchase()

