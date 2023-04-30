from model.address import Address
from repository.address import AddressRepository
from util.exception.custom_exception import AddressDeletionError

address_repository = AddressRepository()


class AddressService:

    @staticmethod
    def delete_address_by_id(address_id):
        address_exists = address_repository.delete_address_by_id(address_id)
        if address_exists:
            return True
        else:
            raise AddressDeletionError(address_id)

    @staticmethod
    def create_new_address(zip_code, street, number, complement, neighborhood, city, state, country):
        new_address = Address(
            street=street,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country
        )
        if new_address:
            return new_address
        else:
            raise AddressCreationError()
