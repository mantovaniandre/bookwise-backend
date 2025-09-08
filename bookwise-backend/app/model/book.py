from sqlalchemy import Column, Integer, String, DateTime, func, Numeric, Text, Boolean
from sqlalchemy.orm import relationship
from configuration.database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(200), nullable=False, index=True)
    isbn = Column(String(17), nullable=True, unique=True, index=True)  # ISBN-13 with hyphens
    
    # Book details
    publication_year = Column(Integer, nullable=True)
    edition = Column(String(50), nullable=True)
    publisher = Column(String(100), nullable=True)
    book_format = Column(String(30), nullable=True)  # hardcover, paperback, ebook, audiobook
    binding = Column(String(30), nullable=True)
    language = Column(String(30), default='English')
    country = Column(String(50), nullable=True)
    pages = Column(Integer, nullable=True)
    
    # Inventory and pricing
    stock_quantity = Column(Integer, default=0, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, index=True)
    cost_price = Column(Numeric(10, 2), nullable=True)  # For profit calculation
    
    # Content and media
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    preview_url = Column(String(500), nullable=True)  # Preview/sample URL
    
    # Categories and classification
    category = Column(String(50), nullable=True, index=True)
    subcategory = Column(String(50), nullable=True)
    genre = Column(String(50), nullable=True)
    target_audience = Column(String(30), nullable=True)  # adult, young_adult, children
    
    # Status and visibility
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_bestseller = Column(Boolean, default=False)
    
    # SEO and metadata
    slug = Column(String(250), nullable=True, unique=True, index=True)
    meta_title = Column(String(200), nullable=True)
    meta_description = Column(String(500), nullable=True)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    comments = relationship('Comment', back_populates='book', cascade='all, delete-orphan')

    def __init__(self, title, author, price, isbn=None, publication_year=None, 
                 edition=None, publisher=None, book_format=None, binding=None, 
                 language='English', country=None, pages=None, stock_quantity=0, 
                 image_url=None, description=None, category=None, cost_price=None):
        self.title = title
        self.author = author
        self.price = price
        self.isbn = isbn
        self.publication_year = publication_year
        self.edition = edition
        self.publisher = publisher
        self.book_format = book_format
        self.binding = binding
        self.language = language
        self.country = country
        self.pages = pages
        self.stock_quantity = stock_quantity
        self.image_url = image_url
        self.description = description
        self.category = category
        self.cost_price = cost_price
        
        # Generate slug from title
        if title:
            self.slug = self._generate_slug(title)

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}', " \
               f"price=${self.price}, stock={self.stock_quantity})>"

    def _generate_slug(self, title):
        """Generate URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = slug.strip('-')
        return slug[:240]  # Limit length

    @property
    def is_in_stock(self):
        """Check if book is in stock"""
        return self.stock_quantity > 0

    @property
    def profit_margin(self):
        """Calculate profit margin if cost_price is available"""
        if self.cost_price and self.price:
            return ((self.price - self.cost_price) / self.price) * 100
        return None

    def get_average_rating(self):
        """Calculate average rating from comments"""
        if not self.comments:
            return None
        ratings = [comment.rating for comment in self.comments if comment.rating]
        return sum(ratings) / len(ratings) if ratings else None

    def get_review_count(self):
        """Get number of reviews"""
        return len([comment for comment in self.comments if comment.comment])

    def reduce_stock(self, quantity):
        """Reduce stock quantity (for purchases)"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False

    def increase_stock(self, quantity):
        """Increase stock quantity (for restocking)"""
        self.stock_quantity += quantity

    def to_dict(self, include_relationships=False):
        """
        Convert book to dictionary
        
        Args:
            include_relationships: Whether to include related data like comments
        """
        book_dict = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "edition": self.edition,
            "publisher": self.publisher,
            "book_format": self.book_format,
            "binding": self.binding,
            "language": self.language,
            "country": self.country,
            "pages": self.pages,
            "stock_quantity": self.stock_quantity,
            "price": float(self.price),
            "cost_price": float(self.cost_price) if self.cost_price else None,
            "description": self.description,
            "image_url": self.image_url,
            "preview_url": self.preview_url,
            "category": self.category,
            "subcategory": self.subcategory,
            "genre": self.genre,
            "target_audience": self.target_audience,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "is_bestseller": self.is_bestseller,
            "slug": self.slug,
            "meta_title": self.meta_title,
            "meta_description": self.meta_description,
            "tags": self.tags.split(',') if self.tags else [],
            "is_in_stock": self.is_in_stock,
            "profit_margin": self.profit_margin,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        
        if include_relationships:
            book_dict["average_rating"] = self.get_average_rating()
            book_dict["review_count"] = self.get_review_count()
            book_dict["comments"] = [comment.to_dict() for comment in self.comments]
            
        return book_dict
