from model.credit_card import CreditCard
from util.exception.custom_exception import CreditCardCreateError


class CreditCardService:
    @staticmethod
    def create_new_credit_card(card_number, type_card, flag, bank, country_bank, card_name, expiration, cvv):
        new_credit_card = CreditCard(
            card_number=card_number,
            type_card=type_card,
            flag=flag,
            bank=bank,
            country_bank=country_bank,
            card_name=card_name,
            expiration=expiration,
            cvv=cvv
        )
        if new_credit_card:
            return new_credit_card
        else:
            raise CreditCardCreateError()
