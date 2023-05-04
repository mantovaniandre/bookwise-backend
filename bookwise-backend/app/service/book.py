from repository.book import BookRepository
from repository.user import UserRepository
from util.exception.custom_exception import MissingRequiredFieldError, InvalidFieldLengthError, UserCannotUpdateBooks, \
    SameDataInDatabaseException, IsbnAlreadyExistsException

book_repository = BookRepository()
user_repository = UserRepository()


class BookService:

    @staticmethod
    def validate_user_data_and_field_sizes(request_data):
        required_fields = ['title', 'author', 'year', 'isbn', 'edition', 'origin', 'book_format',
                           'binding', 'language', 'country', 'pages', 'stock', 'url_img',
                           'description', 'price', 'category']

        max_lengths = {'title': 50, 'author': 50, 'year': 10, 'isbn': 30, 'edition': 30, 'origin': 30,
                       'book_format': 30, 'binding': 30, 'language': 30, 'country': 50, 'pages': 4,
                       'stock': 4, 'url_img': 255, 'description': 255, 'price': 8, 'category': 20}

        for field in required_fields:
            if field not in request_data:
                raise MissingRequiredFieldError(field)
            elif not request_data[field]:
                raise MissingRequiredFieldError(field)
            if field in max_lengths and len(request_data[field]) > max_lengths[field]:
                raise InvalidFieldLengthError(field, max_lengths[field])

    @staticmethod
    def get_book():
        try:
            book = book_repository.get_book()
            return book
        except Exception as e:
            raise e

    @staticmethod
    def get_book_by_id(book_id):
        try:
            book = book_repository.get_book_by_id(book_id)
            book_dict = book.to_dict()
            return book_dict
        except Exception as e:
            raise e

    @staticmethod
    def update_book(request_data, id_user_token, request_book_id):
        different_values = {}
        same_values = {}
        try:
            user = user_repository.get_user_by_id(id_user_token)

            if user.user_type_id == 1:
                BookService.validate_user_data_and_field_sizes(request_data)
                book = book_repository.get_book_by_id(request_book_id)
                supposed_old_book = {
                    'title': book.title,
                    'author': book.author,
                    'year': book.year,
                    'isbn': book.isbn,
                    'edition': book.edition,
                    'origin': book.origin,
                    'book_format': book.book_format,
                    'binding': book.binding,
                    'language': book.language,
                    'country': book.country,
                    'pages': book.pages,
                    'stock': book.stock,
                    'url_img': book.url_img,
                    'description': book.description,
                    'price': book.price,
                    'category': book.category
                }

                supposed_new_book = {
                    'title': request_data['title'],
                    'author': request_data['author'],
                    'year': request_data['year'],
                    'isbn': request_data['isbn'],
                    'edition': request_data['edition'],
                    'origin': request_data['origin'],
                    'book_format': request_data['book_format'],
                    'binding': request_data['binding'],
                    'language': request_data['language'],
                    'country': request_data['country'],
                    'pages': request_data['pages'],
                    'stock': request_data['stock'],
                    'url_img': request_data['url_img'],
                    'description': request_data['description'],
                    'price': request_data['price'],
                    'category': request_data['category']
                }

                for key, value in supposed_old_book.items():
                    new_value_upper = supposed_new_book[key].upper()
                    old_value_upper = value.upper() if value else None
                    if new_value_upper != old_value_upper:
                        different_values[key] = new_value_upper
                        existing_book = book_repository.verify_book_by_isbn(supposed_new_book['isbn'])
                        if existing_book and existing_book.id != book.id:
                            raise IsbnAlreadyExistsException()
                    else:
                        same_values[key] = new_value_upper

                if different_values:
                    book_repository.update_book(book.id, **different_values)
                else:
                    raise SameDataInDatabaseException()

                return True
            else:
                raise UserCannotUpdateBooks(user.user_type_id)
        except Exception as e:
            raise e
