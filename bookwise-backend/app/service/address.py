from model.address import Address
from repository.address import AddressRepository

address_repository = AddressRepository()


class AddressService:
    @staticmethod
    def create_address(**kwargs):
        new_address = Address(**kwargs)
        if new_address:
            return new_address
        else:
            raise ValueError(f"error creating new address.")

    @staticmethod
    def delete_address_by_id(address_id):
        address_exists = address_repository.delete_address_by_id(address_id)
        if address_exists is False:
            raise ValueError(f"error deleting address id: {address_id}.")