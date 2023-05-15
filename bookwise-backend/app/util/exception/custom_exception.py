class AddressDeletionError(Exception):
    def __init__(self, address_id):
        self.address_id = address_id
        super().__init__(f"Error deleting address with ID {address_id}.")


class AddressUpdatingError(Exception):
    def __init__(self, address_id):
        self.address_id = address_id
        super().__init__(f"Error updating address with ID {address_id}.")


class GetAddressByIdOfUserError(Exception):
    def __init__(self, address_id):
        self.address_id = address_id
        super().__init__(f"Error get address by id of user with ID {address_id}.")



class BookDeletionError(Exception):
    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"Error deleting book with ID {book_id}.")


class GetBookByLanguageError(Exception):
    def __init__(self, language):
        self.language = language
        super().__init__(f"Error finding book with language: {language}.")


class GetBookByAuthorError(Exception):
    def __init__(self, author):
        self.author = author
        super().__init__(f"Error finding book with author: {author}.")


class GetBookByTitleError(Exception):
    def __init__(self, title):
        self.title = title
        super().__init__(f"Error finding book with title: {title}.")

class UserDeletionError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"Error deleting user with ID {user_id}.")


class AddressValidationError(Exception):
    def __init__(self, message="Address validation error."):
        self.message = message
        super().__init__(self.message)


class AddressCreationError(Exception):
    def __init__(self, message="Error creating new address. Please check the provided data and try again."):
        self.message = message
        super().__init__(self.message)


class AddressSaveError(Exception):
    def __init__(self, message="Failed to save address."):
        self.message = message
        super().__init__(self.message)


class CreditCardSaveError(Exception):
    def __init__(self, message="Error saving credit card."):
        self.message = message
        super().__init__(self.message)


class CreditCardUpdatingError(Exception):
    def __init__(self, message="Error updating credit card."):
        self.message = message
        super().__init__(self.message)


class CreditCardCreateError(Exception):
    def __init__(self, message="Error creating credit card."):
        self.message = message
        super().__init__(self.message)


class DatabaseError(Exception):
    def __init__(self, e):
        self.e = e
        super().__init__(f"Internal database error: '{e}'")


class GenderValidationError(ValueError):
    def __init__(self, gender):
        self.cpf = gender
        super().__init__(f"Invalid gender: '{gender}'. Must be either 'MASCULINE' or 'FEMININE'.")


class GenderNotFoundError(Exception):
    def __init__(self, gender):
        self.cpf = gender
        super().__init__(f"The gender: '{gender}' not exists to found id.")


class LoginError(Exception):
    def __init__(self, message="Error when logging in."):
        self.message = message
        super().__init__(self.message)


class MissingCredentialsError(Exception):
    def __init__(self, message="Email and password are required"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid Credential."):
        self.message = message
        super().__init__(self.message)


class PasswordCheckError(Exception):
    def __init__(self, message="Failed password check."):
        self.message = message
        super().__init__(self.message)


class TokenGenerationError(Exception):
    def __init__(self, e):
        self.e = e
        super().__init__(f"Error generating token: {e}")


class InternalError(Exception):
    def __init__(self, e):
        self.e = e
        super().__init__(f"Internal error: {e}")


class UserNotFoundEmailError(Exception):
    def __init__(self, email):
        self.email = email
        super().__init__(f"User with {email} not found.")


class BooksNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"Books not found.")


class CPFHasToHaveOnlyNumbers(Exception):
    def __init__(self, message="CPF should contain only numbers."):
        self.message = message
        super().__init__(self.message)


class UserNotFoundIdError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found.")


class PurchaseNotFoundIdError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found purchase.")


class BookNotFoundIdError(Exception):
    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"The book {book_id} not found.")


class UserCannotUpdateBookError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"user the id {user_id} cannot update books.")


class UserCannotCreateBookError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f"user the id {user_id} cannot update books.")


class InvalidCpfSizeError(ValueError):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"The CPF {cpf} has an invalid size.")


class UserCPFError(Exception):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"User with CPF {cpf} already exists in the database.")


class InvalidEmailFormatError(ValueError):
    def __init__(self, email):
        self.email = email
        super().__init__(f"Invalid email format: {email}")


class InvalidPasswordError(ValueError):
    def __init__(self, message="Invalid password."):
        self.message = message
        super().__init__(self.message)


class InvalidFieldLengthError(Exception):
    def __init__(self, field_name, max_length):
        self.field_name = field_name
        self.max_length = max_length
        super().__init__(f"The field '{field_name}' has an invalid length. Maximum length allowed is {max_length}.")


class IsbnAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__(f"The isbn already exists.")


class NewUserCreationError(Exception):
    def __init__(self, message="Error creating new user."):
        self.message = message
        super().__init__(self.message)


class NewBookCreationError(Exception):
    def __init__(self, message="Error creating new book."):
        self.message = message
        super().__init__(self.message)


class UserCreationError(Exception):
    def __init__(self, message="Error creating user."):
        self.message = message
        super().__init__(self.message)


class PurchaseCreationError(Exception):
    def __init__(self, message="Error creating purchase."):
        self.message = message
        super().__init__(self.message)


class BookCreationError(Exception):
    def __init__(self, message="Error creating book."):
        self.message = message
        super().__init__(self.message)

class UserUpdateError(Exception):
    def __init__(self, e):
        self.e = e
        super().__init__(f"Error update user:'{e}'")


class PasswordEncryptionError(Exception):
    def __init__(self, e):
        self.e = e
        super().__init__(f"Error encrypting password:'{e}'")


class DuplicateEmailError(ValueError):
    def __init__(self, email):
        self.email = email
        super().__init__(f"Email '{email}' already exists.")


class MissingRequiredFieldError(ValueError):
    def __init__ (self, field):
        self.field = field
        super().__init__(f"Required field '{field}' not provided or cannot be empty.")


class CPFLengthError(ValueError):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"The cpf {cpf} must have exactly 11 digits.")


class DuplicateCPFError(ValueError):
    def __init__(self, cpf):
        self.cpf = cpf
        super().__init__(f"CPF {cpf} already exists.")


class SameDataInDatabaseException(Exception):
    def __init__(self, message="The data is the same as in the database. No changes were made."):
        self.message = message
        super().__init__(self.message)


class CreatingBookISBNError(ValueError):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"error creating book: {isbn} already exists.")


class InvalidUserTypeError(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(f"The user_type: '{description}' is invalid. Please choose either 'CLIENT' or 'ADMIN'.")


class UserTypeNotFoundError(Exception):
    def __init__(self, description):
        self.description = description
        super().__init__(f"The user_type: '{description}' was not found.")


class UserTypeCreationError(Exception):
    def __init__(self, message="User type creation failed."):
        self.message = message
        super().__init__(self.message)