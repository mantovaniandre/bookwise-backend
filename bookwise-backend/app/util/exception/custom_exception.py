class CPFAlreadyExists(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        self.message = f"CPF {cpf} already exists."
        super().__init__(self.message)


class EmailAlreadyExists(Exception):
    def __init__(self, email):
        self.cpf = email
        self.message = f"Email {email} already exists."
        super().__init__(self.message)


class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ValidateUserDataError(Exception):
    def __init__(self, field):
        self.field = field
        self.message = f"Required field '{field}' not provided."
        super().__init__(self.message)


class ValidateUsertypeError(Exception):
    def __init__(self, description):
        self.description = description
        self.message = f"The usertype: '{description}' not exists."
        super().__init__(self.message)


class ValidateGenderError(Exception):
    def __init__(self, description):
        self.description = description
        self.message = f"The usertype: '{description}' not exists."
        super().__init__(self.message)


class DescriptionUsertypeError(Exception):
    def __init__(self, description):
        self.description = description
        self.message = f"The usertype: '{description}' not exists to found id."
        super().__init__(self.message)


class DescriptionGenderError(Exception):
    def __init__(self, description):
        self.description = description
        self.message = f"The gender: '{description}' not exists to found id."
        super().__init__(self.message)


class NewUserError(Exception):
    def __init__(self):
        self.message = f"error creating new user."
        super().__init__(self.message)


class NewAddressError(Exception):
    def __init__(self):
        self.message = f"error creating new address."
        super().__init__(self.message)


class DeleteAddressError(Exception):
    def __init__(self, address_id):
        self.address_id = address_id
        self.message = f"error deleting address id: {address_id}."
        super().__init__(self.message)


class RegisterUserError(Exception):
    def __init__(self, e):
        self.e = e
        self.message = f"error registering user: {e}"
        super().__init__(self.message)