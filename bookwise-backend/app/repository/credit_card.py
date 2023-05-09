from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from configuration.database import Session
from model.credit_card import CreditCard
from util.exception.custom_exception import DatabaseError, CreditCardSaveError, CreditCardUpdatingError


class CreditCardRepository:
    @staticmethod
    def save_credit_card(credit_card):
        with Session() as session:
            try:
                session.add(credit_card)
                session.commit()
                session.refresh(credit_card)
                credit_card_id = credit_card.id
                if credit_card_id is not None:
                    return credit_card_id
                else:
                    session.rollback()
                    raise CreditCardSaveError()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def update_credit_card(table_name, credit_card_id, **update_values):
        with Session() as session:
            try:
                credit_card = session.query(CreditCard).filter_by(id=credit_card_id).first()
                if not credit_card:
                    raise CreditCardUpdatingError(credit_card_id)
                for column, value in update_values.items():
                    setattr(credit_card, column, value)
                credit_card.last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))

    @staticmethod
    def get_credit_card_by_id_of_user(user_id):
        with Session() as session:
            try:
                credit_card = session.query(CreditCard).filter_by(id=user_id).first()
                if credit_card is not None:
                    return credit_card
                else:
                    return False
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(str(e))
