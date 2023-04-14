from model.address import Address
from repository.address import AddressRepository

address_repository = AddressRepository()


class AddressService:

    @staticmethod
    def delete_address_by_id(address_id):
        address_exists = address_repository.delete_address_by_id(address_id)
        if address_exists is False:
            raise ValueError(f"error deleting address id: {address_id}.")

    @staticmethod
    def create_new_address(zipCode, street, number, complement, neighborhood, city, state, country):
        new_address = Address(
            street=street,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            city=city,
            state=state,
            zipcode=zipCode,
            country=country
        )
        if new_address:
            return new_address
        else:
            raise ValueError(f"error creating new address.")
