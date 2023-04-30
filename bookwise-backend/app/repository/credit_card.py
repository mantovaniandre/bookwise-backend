from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from configuration.database import Session
from util.exception.custom_exception import DatabaseError, CreditCardSaveError

# created instances
session = Session()


class CreditCardRepository:
    @staticmethod
    def save_credit_card(credit_card):
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
        except Exception as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()

    @staticmethod
    def update_credit_card(table_name, credit_card_id, **update_values):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"UPDATE {table_name} SET last_update = '{now}', "
        for column, value in update_values.items():
            query += f"{column} = '{value}', "
        query = query[:-2]
        query += f" WHERE id = {credit_card_id};"
        query = text(query)
        try:
            session.execute(query)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError(str(e))
        finally:
            session.close()