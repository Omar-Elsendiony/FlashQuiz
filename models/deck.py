import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import relationship

# Association table for deck-flashcard relationship
deck_flashcard = Table('deck_flashcard', Base.metadata,
    Column('deck_id', String(60), ForeignKey('deck.id'), primary_key=True),
    Column('flashcard_id', String(60), ForeignKey('flashcard.id'), primary_key=True)
)

class Deck(BaseModel, Base):
    """Flashcard Deck Model"""
    __tablename__ = 'deck'
    
    name = Column(String(128), nullable=False)
    description = Column(Text)
    # is_public = Column(Integer, default=1)  # 1 for public, 0 for private
    view_count = Column(Integer, default=0)

    # Relationships
    creator_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    creator = relationship('User', backref='decks_created')
    
    category_id = Column(String(60), ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='decks')
    
    # Many-to-many relationship with flashcards
    flashcards = relationship('Flashcard', 
                            secondary=deck_flashcard,
                            back_populates='decks')

    # Many-to-many relationship for users who have favorited this deck
    favorited_by = relationship('User',
                            secondary='user_favorite_decks',
                            back_populates='favorited_decks')


