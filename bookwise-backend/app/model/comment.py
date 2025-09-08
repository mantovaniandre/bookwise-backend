from configuration.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    
    # Review content
    comment = Column(Text, nullable=True)  # Optional review text
    rating = Column(Integer, nullable=False)  # 1-5 star rating
    title = Column(String(200), nullable=True)  # Optional review title
    
    # Status and moderation
    is_approved = Column(Integer, default=1)  # 0=pending, 1=approved, 2=rejected
    is_featured = Column(Integer, default=0)  # Featured review
    helpful_count = Column(Integer, default=0)  # Helpful votes
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='comments')
    book = relationship('Book', back_populates='comments')

    def __init__(self, user_id, book_id, rating, comment=None, title=None):
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.comment = comment
        self.title = title

    def __repr__(self):
        return f"<Comment(id={self.id}, user_id={self.user_id}, " \
               f"book_id={self.book_id}, rating={self.rating})>"

    @property
    def is_positive(self):
        """Check if this is a positive review (4+ stars)"""
        return self.rating >= 4

    def mark_helpful(self):
        """Increment helpful count"""
        self.helpful_count += 1

    def to_dict(self, include_user=False, include_book=False):
        """
        Convert comment to dictionary
        
        Args:
            include_user: Include user details
            include_book: Include book details
        """
        comment_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "comment": self.comment,
            "rating": self.rating,
            "title": self.title,
            "is_approved": self.is_approved,
            "is_featured": bool(self.is_featured),
            "helpful_count": self.helpful_count,
            "is_positive": self.is_positive,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
        
        if include_user and self.user:
            comment_dict["user"] = {
                "id": self.user.id,
                "full_name": self.user.full_name,
                "first_name": self.user.first_name
            }
            
        if include_book and self.book:
            comment_dict["book"] = {
                "id": self.book.id,
                "title": self.book.title,
                "author": self.book.author
            }
            
        return comment_dict