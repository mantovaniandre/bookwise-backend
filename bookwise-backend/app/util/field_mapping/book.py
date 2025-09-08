from model.book import Book

# Sample books data for development
books = [
    Book(
        title="The Hunger Games",
        author="Suzanne Collins",
        price=22.45,
        isbn="9780439023481",
        publication_year=2008,
        edition="1st",
        publisher="Scholastic Press",
        book_format="ebook",
        binding="Sewn Binding",
        language="English",
        country="United States",
        pages=384,
        stock_quantity=100,
        image_url="https://m.media-amazon.com/images/I/414fBKKVniL._SY344_BO1,204,203,200_QL70_ML2_.jpg",
        description="In A Dystopian North America Katniss Volunteers To Compete In A Televised Survival "
                    "Game Replacing Her Younger Sister The Game Is Run By The Rulers Of Panem To Maintain "
                    "Control Over The Twelve Districts.",
        category="Adventure"
    ),
    Book(
        title="The Da Vinci Code",
        author="Dan Brown",
        price=12.13,
        isbn="9780307474278",
        publication_year=2003,
        edition="1st",
        publisher="Doubleday",
        book_format="ebook",
        binding="Perfect Binding",
        language="English",
        country="United States",
        pages=689,
        stock_quantity=50,
        image_url="https://m.media-amazon.com/images/I/51hYdKyWYqL._SY346_.jpg",
        description="Professor Robert Langdon And Cryptographer Sophie Neve Must Decipher A Deadly "
                    "Web Of Deceit Involving The Works Of Leonardo Da Vinci After The Curator Of The "
                    "Louvre Is Found Murdered In The Museums Halls.",
        category="Adventure"
    ),
    Book(
        title="The Lord of the Rings: The Fellowship of the Ring",
        author="J.R.R. Tolkien",
        price=25.33,
        isbn="9780547928210",
        publication_year=1954,
        edition="1st",
        publisher="George Allen & Unwin",
        book_format="ebook",
        binding="Sewn Binding",
        language="English",
        country="United Kingdom",
        pages=432,
        stock_quantity=80,
        image_url="https://m.media-amazon.com/images/I/61mn09OvTQL._AC_UY327_FMwebp_QL65_.jpg",
        description="The First Volume In Jrr Tolkiens Epic Adventure The Lord Of The Rings One Ring To Rule "
                    "Them All One Ring To Find Them One Ring To Bring Them All And In The Darkness Bind Them.",
        category="Adventure"
    ),
    Book(
        title="Pride and Prejudice",
        author="Jane Austen",
        price=12.56,
        isbn="9780486284736",
        publication_year=1813,
        edition="1st Edition",
        publisher="T. Egerton",
        book_format="ebook",
        binding="Perfect",
        language="English",
        country="United Kingdom",
        pages=352,
        stock_quantity=10,
        image_url="https://m.media-amazon.com/images/I/81FOTF7SJvL._AC_UY327_FMwebp_QL65_.jpg",
        description="Jane Austens Classic Love Story Between Elizabeth Bennet And Mr Darcy Where Love Blooms Sometimes "
                    "Against Their Own Pride And Prejudices.",
        category="Romance"
    ),
    Book(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        price=15.40,
        isbn="9780547928227",
        publication_year=1937,
        edition="1st",
        publisher="George Allen & Unwin",
        book_format="ebook",
        binding="Perfect",
        language="English",
        country="United Kingdom",
        pages=310,
        stock_quantity=50,
        image_url="https://m.media-amazon.com/images/I/91M9xPIf10L._AC_UY327_FMwebp_QL65_.jpg",
        description="The Hobbit Bilbo Baggins Embarks On An Epic Adventure With A Group Of Dwarves To Reclaim "
                    "Their Stolen Treasure From A Dragon.",
        category="Adventure"
    )
]