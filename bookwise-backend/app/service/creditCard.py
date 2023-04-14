from model.creditCard import CreditCard


class CreditCardService:
    @staticmethod
    def create_new_credit_card(cardNumber, typeCard, flag, bank, countryBank, cardName, expiration, cvv):
        new_credit_card = CreditCard(
            cardNumber=cardNumber,
            typeCard=typeCard,
            flag=flag,
            bank=bank,
            countryBank=countryBank,
            cardName=cardName,
            expiration=expiration,
            cvv=cvv
        )
        if new_credit_card:
            return new_credit_card
        else:
            raise ValueError(f"error creating new credit card.")