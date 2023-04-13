from model.address import Address
from repository.address import AddressRepository

address_repository = AddressRepository()


class AddressService:

    @staticmethod
    def delete_address_by_id(address_id):
        address_exists = address_repository.delete_address_by_id(address_id)
        if address_exists is False:
            raise ValueError(f"error deleting address id: {address_id}.")
