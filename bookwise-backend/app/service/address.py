from model.address import Address


class AddressService:
    @staticmethod
    def create_address(**kwargs):
        new_address = Address(**kwargs)
        return new_address
