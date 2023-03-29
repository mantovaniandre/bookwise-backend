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
