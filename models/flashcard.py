import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import relationship

class Flashcard(BaseModel, Base):
    """Flashcard Model"""
    __tablename__ = 'flashcard'
    
    front = Column(String(255), nullable=False)
    back = Column(String(255), nullable=False)
    
    # creator_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    # creator = relationship('User', backref='flashcards_created')
    
    # category_id = Column(String(60), ForeignKey('category.id'), nullable=False)
    # category = relationship('Category', backref='flashcards')
    
    # Many-to-many relationship with decks
    decks = relationship('Deck',
                        secondary='deck_flashcard',
                        back_populates='flashcards')
    
    # Many-to-many relationship for users who have favorited this flashcard
    # favorited_by = relationship('User', 
    #                         secondary='user_favorite_flashcards', 
    #                         back_populates='favorited_flashcards')
