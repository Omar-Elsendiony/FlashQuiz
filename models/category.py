import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Text, Table
from sqlalchemy.orm import relationship





class Category(BaseModel, Base):
    __tablename__ = 'category'
    
    # id = Column(String(60), autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    
    # quizzes = relationship('Quiz', backref='category-quiz')
    # flashcards = relationship('Flashcard', backref='category-flashcard')
