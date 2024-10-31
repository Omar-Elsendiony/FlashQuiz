import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import relationship

class Flashcard(BaseModel, Base):
    __tablename__ = 'flashcard'
    # id = Column(Integer, primary_key=True)
    front = Column(String(255), nullable=False)
    back = Column(String(255), nullable=False)
    view_count = Column(Integer, default=0)
    
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # creator = relationship('User', backref='flashcards-created')
    
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='flashcards-category')
    
    favorited_by = relationship('User', 
                                secondary='user_favorite_flashcards', 
                                back_populates='favorited_flashcards',
                                overlaps="favorited_by")
