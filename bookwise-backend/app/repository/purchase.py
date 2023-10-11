from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.purchase import Purchase
from util.exception.custom_exception import DatabaseError, PurchaseCreationError, PurchaseNotFoundIdError


class PurchaseRepository:
    @staticmethod
    def create_purchase(purchase):
        with Session() as session:
            try:
                session.add(purchase)
                session.commit()
                session.refresh(purchase)
                user_id = purchase.id
                if user_id is not None:
                    return True
                else:
                    session.rollback()
                    raise PurchaseCreationError()
            except Exception as e:
                session.rollback()
                raise DatabaseError(str(e))

    def get_purchase_by_id_user(user_id):
        with Session() as session:
            try:
                purchases = session.query(Purchase).filter_by(user_id=user_id).all()
                if not purchases:
                    raise PurchaseNotFoundIdError(user_id)
                purchases_dict = [purchase.to_dict() for purchase in purchases]
                return purchases_dict
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    def get_purchase_by_id_user_and_id_book(user_id, book_id):
        with Session() as session:
            try:
                purchases = session.query(Purchase).filter_by(user_id=user_id).all()
                if not purchases:
                    raise PurchaseNotFoundIdError(user_id)
                purchases_dict = [purchase.to_dict() for purchase in purchases]
                return purchases_dict
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))
