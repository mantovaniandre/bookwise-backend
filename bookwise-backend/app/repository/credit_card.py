from configuration.database import Session

# created instances
session = Session()


class CreditCardRepository:
    @staticmethod
    def save_credit_card(new_credit_card):
        try:
            session.add(new_credit_card)
            session.commit()
            session.refresh(new_credit_card)
            credit_card_id = new_credit_card.id
            if credit_card_id is not None:
                return credit_card_id
            else:
                session.rollback()
                return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

    @staticmethod
    def update_credit_card(table_name, credit_card_id, **update_values):
        query = f"UPDATE {table_name} SET "
        for column, value in update_values.items():
            query += f"{column}='{value}', "
        query = query[:-2]
        query += f"WHERE id = {credit_card_id};"
        session.execute(query)
        session.commit()