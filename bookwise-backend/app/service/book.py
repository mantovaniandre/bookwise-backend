from repository.book import BookRepository

book_repository = BookRepository()


class BookService:
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
