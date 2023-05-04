from model.book import Book
from model.gender import Gender
from model.user_type import UserType
from configuration.database import Base, engine, Session


def create_user_type():
    session = Session()
    employee = session.query(UserType).filter_by(description='ADMIN').first()
    admin = session.query(UserType).filter_by(description='CLIENT').first()
    if not employee:
        session.add(UserType(description='ADMIN'))
    if not admin:
        session.add(UserType(description='CLIENT'))
    session.commit()


def create_gender():
    session = Session()
    masculine = session.query(Gender).filter_by(description='MASCULINE').first()
    feminine = session.query(Gender).filter_by(description='FEMININE').first()
    if not masculine:
        session.add(Gender(description='MASCULINE'))
    if not feminine:
        session.add(Gender(description='FEMININE'))
    session.commit()


def insert_books(books: list[Book]):
    session = Session()
    try:
        for book in books:
            book_isbn = book.isbn.upper()
            existing_book = session.query(Book).filter(Book.isbn == book_isbn).first()
            if existing_book:
                print(f"Skipping book with ISBN {book_isbn} - already exists in database")
            else:
                book.title = book.title.upper()
                book.year = book.year.upper()
                book.author = book.author.upper()
                book.isbn = book_isbn.upper()
                book.edition = book.edition.upper()
                book.origin = book.origin.upper()
                book.book_format = book.book_format.upper()
                book.binding = book.binding.upper()
                book.language = book.language.upper()
                book.country = book.country.upper()
                book.pages = book.pages.upper()
                book.stock = book.stock.upper()
                book.url_img = book.url_img
                book.description = book.description.upper()
                book.price = book.price.upper()
                book.category = book.category.upper()
                session.add(book)
        session.commit()
        print('Books inserted successfully!')
    except Exception as e:
        session.rollback()
        print(f'Error inserting books: {str(e)}')
    finally:
        session.close()



def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)